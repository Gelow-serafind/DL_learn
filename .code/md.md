#### 测试一下
```c
switch (ctrl->state)
	{
			/**< 0行走轮处于初始上电状态 */
		case WHEEL_MANAGE_STATE_INIT:
			/*! 初始延时2S并且使能数据上传保证主控数据记录后进入正常流程 */
			if ((elapse_time >= 2000) && (TRUE == ctrl->b_upload_enable))
			{
				if (ctrl->action_level > EXCEPTION_ACTION_NORMAL)
				{
					action_level_max = EXCEPTION_ACTION_NORMAL;
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL;
				}
				else
				{
					if (FALSE == ctrl->b_align_init)
					{
						ctrl->state = WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_ALIGN;
					}
					else
					{
						ctrl->state = WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_NORMAL;
					}
				}

				ctrl->state_change_start_time = time_get_mono_ms();
			}

			break;
			/**< 1异常恢复后，如果行走轮电机不需要重新位置初始化，等待行走模块静止，才能切到NORMAL状态,此时可以接收行走轮STOP命令 */
		case WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_NORMAL:
			/*! 如果超过2S行走轮还未停止，也强制设置行走轮速度0，避免出现在坡上时急停触发瞬间恢复时一直溜坡不能锁住的情况 */
			if ((elapse_time >= 2000) || (TRUE == ctrl->b_wheel_stop))
			{
				wheel_set_all_motor_vel_0();
				ctrl->state = WHEEL_MANAGE_STATE_DELAY_TO_NORMAL;
				ctrl->state_change_start_time = time_get_mono_ms();
			}

			break;
			/**< 2异常恢复后，如果行走轮电机需要重新位置初始化，等待行走模块静止后才能接收行走轮STOP命令 */
		case WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_ALIGN:
			if (TRUE == ctrl->b_wheel_stop)
			{
				wheel_set_all_motor_vel_0();
				ctrl->state = WHEEL_MANAGE_STATE_WAIT_ALIGN;
				ctrl->state_change_start_time = time_get_mono_ms();
			}

			break;
			/**< 3等待所有驱动轮都已接收到控制命令，开始位置初始化动作 */
		case WHEEL_MANAGE_STATE_WAIT_ALIGN:
			if (TRUE == ctrl->b_align_init)
			{
				ctrl->state = WHEEL_MANAGE_STATE_DELAY_TO_NORMAL;
				ctrl->state_change_start_time = time_get_mono_ms();
			}
		
			break;
			/**< 4异常恢复后，延时进入正常模式 */
		case WHEEL_MANAGE_STATE_DELAY_TO_NORMAL:
			if ((elapse_time >= 2000) && (TRUE == ctrl->b_wheel_stop))
			{
				if (FALSE == ctrl->b_need_cali_exist)
				{
					ctrl->state = WHEEL_MANAGE_STATE_NORMAL;
				}
				else
				{
					ctrl->state = WHEEL_MANAGE_STATE_WAIT_CALI_START;
				}

				ctrl->state_change_start_time = time_get_mono_ms();
			}
		
			break;

        case WHEEL_MANAGE_STATE_WAIT_CALI_START:
			if (TRUE == ctrl->b_all_cali_ok)
			{
				ctrl->cali_try_cnt = 0;
				ctrl->state = WHEEL_MANAGE_STATE_NORMAL;
				ctrl->state_change_start_time = time_get_mono_ms();
			}
			else
			{
				/*! 轮组连续位置校正次数超过5次，就不再自动重新初始化校正，除非安全保护状态由触发变为不触发 */
				if (ctrl->cali_try_cnt < 5)
				{
					wheel_manage_cali_start();
					ctrl->state = WHEEL_MANAGE_STATE_CALI;
					ctrl->state_change_start_time = time_get_mono_ms();
					ctrl->cali_try_cnt++;
				}
			}
			
			break;
			/**< 10行走模块处于轮组旋转角度校正过程中 */
		case WHEEL_MANAGE_STATE_CALI:
			if (TRUE == ctrl->b_all_cali_ok)
			{
				ctrl->cali_try_cnt = 0;
				ctrl->state = WHEEL_MANAGE_STATE_NORMAL;
				for (i = 0; i < ctrl->group_cnt; i++)
				{
					group = &ctrl->group_ctrl[i];

					if (FALSE == group->b_exist)
					{
						continue;
					}					
					wheel_group_set_cur_limit(group, FALSE);
				}

				ctrl->state_change_start_time = time_get_mono_ms();
			}
			else
			{
				wheel_manage_cali_check_process();
			}

			break;
			/**< 5行走模块完全正常，可以接收相关命令 */
		case WHEEL_MANAGE_STATE_NORMAL:
			if (ctrl->action_level > EXCEPTION_ACTION_NORMAL)
			{
				if (EXCEPTION_ACTION_LEVEL1 == ctrl->action_level)
				{
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL_WAIT_HOST_CTRL_STOP;
				}
				else if (EXCEPTION_ACTION_LEVEL2 == ctrl->action_level)
				{
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL_WAIT_RCU_CTRL_STOP;
					wheel_set_all_motor_stop();
				}
				else
				{
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL;
				}

				ctrl->state_change_start_time = time_get_mono_ms();
			}
			else
			{
				/*! 如果正常模式下发现轮组位置校正失败，则需要切换状态到异常状态后，重新进行校正动作 */
				if ((TRUE == ctrl->b_need_cali_exist)
					&& (FALSE == ctrl->b_all_cali_ok))
				{
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL_WAIT_RCU_CTRL_STOP;
					wheel_set_all_motor_stop();
					ctrl->state_change_start_time = time_get_mono_ms();
				}
			}
		
			break;

        case WHEEL_MANAGE_STATE_ABNORMAL_WAIT_HOST_CTRL_STOP:
			if ((ctrl->action_level > EXCEPTION_ACTION_LEVEL2)
				|| (TRUE == ctrl->b_wheel_stop))
			{
				ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL;
				ctrl->state_change_start_time = time_get_mono_ms();
			}
			else if ((EXCEPTION_ACTION_LEVEL2 == ctrl->action_level)
					|| (elapse_time >= ctrl->host_ctrl_stop_timeout))
			{
				ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL_WAIT_RCU_CTRL_STOP;
				wheel_set_all_motor_stop();
				ctrl->state_change_start_time = time_get_mono_ms();
			}

			break;
			/**< 7急停或碰撞触发，等待RCU控制所有行走轮停止 */		
		case WHEEL_MANAGE_STATE_ABNORMAL_WAIT_RCU_CTRL_STOP:
			if ((ctrl->action_level > EXCEPTION_ACTION_LEVEL2)
				|| (TRUE == ctrl->b_wheel_stop)
				|| (elapse_time >= ctrl->host_ctrl_stop_timeout))
			{
				/*! 超时检测到行走轮还未停止，则直接FREERUN所有电机 */	
				if (elapse_time >= ctrl->host_ctrl_stop_timeout)
				{
					wheel_set_all_motor_freerun();
				}

				ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL;
				ctrl->state_change_start_time = time_get_mono_ms();
			}
		
			break;

        case WHEEL_MANAGE_STATE_ABNORMAL:
			if (ctrl->action_level > EXCEPTION_ACTION_NORMAL)
			{
				if (action_level_max < ctrl->action_level)
				{
					action_level_max = ctrl->action_level;

					if ((EXCEPTION_ACTION_LEVEL1 == ctrl->action_level)
						|| (EXCEPTION_ACTION_LEVEL2 == ctrl->action_level))
					{
						/*! 如果安全功能触发，行走轮立即进入FREERUN模式 */
						if (TRUE == b_safe_trigger)
						{
							if (FALSE == b_stop_freerun)
							{
								wheel_set_all_motor_stop();
							}
							else
							{
								wheel_set_all_motor_freerun();
							}
						}
						else
						{
							wheel_set_all_motor_stop();
						}
					}
					else if (EXCEPTION_ACTION_LEVEL3 == ctrl->action_level)
					{
						wheel_set_all_motor_freerun();
					}
				}
				else if (TRUE == b_stop_freerun_edge)
				{
					wheel_set_all_motor_freerun();
				}

				if ((TRUE == ctrl->b_wheel_manual_brake) && (FALSE == b_safeguard_trigger))
				{
					/**< 须在安全未触发情况下进入 */
					ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL_MANUAL_BARKE;
					ctrl->state_change_start_time = time_get_mono_ms();
				}
			}
			else
			{
				if (FALSE == ctrl->b_align_init)
				{
					ctrl->state = WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_ALIGN;
				}
				else
				{
					ctrl->state = WHEEL_MANAGE_STATE_WAIT_STOP_BEFORE_NORMAL;
				}

				ctrl->state_change_start_time = time_get_mono_ms();
				action_level_max = EXCEPTION_ACTION_NORMAL;
			}

			break;


        case WHEEL_MANAGE_STATE_ABNORMAL_MANUAL_BARKE:
			if ((TRUE == b_safeguard_trigger) || (FALSE == ctrl->b_wheel_manual_brake))
			{
				wheel_set_all_motor_brake(0);
				ctrl->b_wheel_brake_open = FALSE;
				ctrl->b_wheel_manual_brake = FALSE;
				ctrl->state = WHEEL_MANAGE_STATE_ABNORMAL;
			}
			else if (FALSE == ctrl->b_wheel_brake_open)               /**< 处于正常状态下的手动模式并且抱闸未打开 */
			{
				wheel_set_all_motor_freerun();
				/*! 进入手动解抱闸状态后，如果行走轮静止或超过2S未静止，直接进行解抱闸动作 */
				if ((elapse_time >= 2000) || (TRUE == ctrl->b_wheel_stop))
				{
					wheel_set_all_motor_brake(1);
					ctrl->b_wheel_brake_open = TRUE;
				}
			}
			
			break;

		default:
			break;
	}

```

### 代码详解
- 这是一个switch
    - case 0
    - case 1

注意： **这是一个注意**
这是 __一个下划线__