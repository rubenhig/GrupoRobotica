/*
 * File:          controlador_3D.c
 * Date:
 * Description:
 * Author:
 * Modifications:
 */

/*
 * You may need to add include files like <webots/distance_sensor.h> or
 * <webots/motor.h>, etc.
 */
#include <webots/robot.h>
#include <math.h>
#include <webots/motor.h>
#include <stdio.h>
#include <webots/utils/ansi_codes.h>

/*
 * You may want to add macros here.
 */
#define TIME_STEP 64

#define movimienºto 0.001

/*
 * This is the main program.
 * The arguments of the main function can be specified by the
 * "controllerArgs" field of the Robot node
 */
int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();

  /*
   * You should declare here WbDeviceTag variables for storing
   * robot devices like this:
   *  WbDeviceTag my_sensor = wb_robot_get_device("my_sensor");
   *  WbDeviceTag my_actuator = wb_robot_get_device("my_actuator");
   */
   
  double time_step = wb_robot_get_basic_time_step();
  WbDeviceTag motor = wb_robot_get_device("linear motor");
  WbDeviceTag motor2 = wb_robot_get_device("linear motor2");
  WbDeviceTag motor3 = wb_robot_get_device("linear motor3");
  
  double target = 0.006;
  double target2 = 0.006;
  double target3 = 0.006;

  //int counter = 0;
  
  int orden = 0;
  int orden2 = 0;
  int orden3 = 0;
  
  
  /* main loop
   * Perform simulation steps of TIME_STEP milliseconds
   * and leave the loop when the simulation is over
   */
  while (wb_robot_step(time_step) != -1) {

    wb_motor_set_position(motor, target);
    wb_motor_set_position(motor2, target2);
    wb_motor_set_position(motor3, target3);
    
    if(orden)
    {
      target += movimiento;
    }else target -= movimiento;
      
    if(orden2)
    {
      target2 += movimiento;
    }else target2 -= movimiento;
    
    
    if(orden3)
    {
      target3 += movimiento;
    }else target3 -= movimiento;
      
    if (target > wb_motor_get_max_position(motor) ||
        target < wb_motor_get_min_position(motor))
    {
        if(orden) orden = 0;
        else orden = 1;
    }
    
    if (target2 > wb_motor_get_max_position(motor2) ||
        target2 < wb_motor_get_min_position(motor2))
    {
      if(orden2) orden2 = 0;
      else orden2 = 1;
    }
        
      
    if (target3 > wb_motor_get_max_position(motor3) ||
        target3 < wb_motor_get_min_position(motor3))
    {
      if(orden3) orden3 = 0;
      else orden3 = 1;
    }
    
  };
  
  // de -0.011 a -0.12
  
  /* Enter your cleanup code here */

  /* This is necessary to cleanup webots resources */
  wb_robot_cleanup();

  return 0;
}
