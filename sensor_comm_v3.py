from cmd_cls_v3 import CMD
import serial
import time
#import logging

class SensorComm(CMD):
        
    def toggle_test_pattern(self):
        response = self.fpga_read(0x53)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                response=self.fpga_write(0x53,data)
            else:
                self.logger.info('Warning, command error, %d'%response['cmd_status'])
        else:
            self.logger.info('Warning, communication link might be broken')
    
    def enable_nuc(self):
        response=self.fpga_write(0x54,1) 
    
    def disable_nuc(self):
        response=self.fpga_write(0x54,0) 
        
    def athena_perform_avg_raw_imgs(self, num_imgs):
        if(num_imgs not in [1,2,4,8,16,32]):
            print('Number of images need to be one of [1,2,4,8,16,32]')
            return
        else:
            num_imgs_dict = {1:0,2:1,4:2,8:3,16:4,32:5}
            data = ((num_imgs_dict[num_imgs] & 0xFF) << 16) | 0x0001
            response=self.fpga_write(0x54,data) 
         
    def toggle_nuc(self):
        response = self.fpga_read(0x54)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                response=self.fpga_write(0x54,data) 
            else:
                self.logger.info('Warning, command error')
#                print('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')
#            print('Warning, communication link might be broken')

    def toggle_row_filter(self):
        response = self.fpga_read(0x55)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                response=self.fpga_write(0x55,data)         
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')
    
    def enable_row_filter(self):
        response = self.fpga_write(0x55, 0x1)
        
    def disable_row_filter(self):
        response = self.fpga_write(0x55, 0x0)

    def toggle_reticle(self):
        response = self.fpga_read(0x56)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                response=self.fpga_write(0x56,data)
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')

    def set_reticle_type(self, reticle_type):
        response=self.fpga_write(0x66, reticle_type)
        if(response!=None):
            if(response['cmd_status']==0):
                self.logger.info('Set reticle type to %d'%reticle_type)
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')

    def move_reticle_left(self, pos=1):
        pass
    def move_reticle_right(self, pos=1):
        pass                 
    def move_reticle_up(self, pos=1):
        pass
    def move_reticle_down(self, pos=1):
        pass

    def toggle_palette(self):
        response = self.fpga_read(0x57)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                self.fpga_write(0x57,data)
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')
                

    def set_palette(self, palette_type):
        response=self.fpga_write(0x58, palette_type)

    def toggle_sharpening(self):
        response = self.fpga_read(0x62)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                self.fpga_write(0x62,data)    
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')
    
    def set_sharpening_level(self, value):
        data = 0x280000000 | (value & 0xFF)
        response = self.fpga_write(0x61, data)
    
    def enable_edge_filter(self):
        response = self.fpga_write(0x50,1)
        response = self.fpga_write(0x4f,0x2c0020)
        
    def disable_edge_filter(self):
        response = self.fpga_write(0x50,0)
        
    def toggle_blurring(self):
        response = self.fpga_read(0x64)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                self.fpga_write(0x64,data)    
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')

    def switch_polarity(self):
        response = self.fpga_read(0x52)
        if(response!=None):
            if(response['cmd_status']==0):
                data = 1-response['data'][-1]
                self.fpga_write(0x52,data)   
            else:
                self.logger.info('Warning, command error')
        else:
            self.logger.info('Warning, communication link might be broken')
    
    def ping_device(self):
        response = self.ping(5)
        if(response!=None):
            return True
        else:
            return False

    def select_agc_mode(self, mode):
    		self.fpga_write(0x51, mode)
          
    def set_digital_zoom(self, zoom):
        self.fpga_write(0x65,1)    
        if(zoom=='1x'):
            self.fpga_write(0x86,0)
        elif(zoom=='2x'):
            self.fpga_write(0x86,1)
        elif(zoom=='4x'):
            self.fpga_write(0x86,2)
        else:
            self.fpga_write(0x86,0)

    def set_brightness(self, brightness_value):
        self.fpga_write(0xd0, brightness_value)

    def set_contrast(self, conrtast_value):
        self.fpga_write(0xd4, conrtast_value)

    def set_brightness_contrast(self, brightness_value, conrtast_value):
        self.set_brightness(brightness_value)
        self.set_contrast(conrtast_value)

    def set_gfid(self, value):
        data = (0x3 << 12) | (value & 0xFFF)
        self.set_spi(data)

    def set_gsk(self, value):
        data = (0x2 << 12) | (value & 0xFFF)
        self.set_spi(data)

    def set_inttime(self, value):
        data = (0x1 << 12) | (value & 0xFFF)
        self.set_spi(data)
    
    def set_detector_param(self, value1, value2, value3):
        self.set_inttime(value1)
        time.sleep(0.5)
        self.set_gfid(value2)
        time.sleep(0.5)
        self.set_gsk(value3)
        time.sleep(0.5)
        
    def set_fuel_gauge_control_reg(self, value):
        self.i2c_write(0x64, 0x01, [value])
    
    def get_fuel_gauge_control_reg(self):
        response = self.i2c_read(0x64, 0x01, 1)
        if(response==None):
            return None
        data = response['data'][0]
        return data
    
    def get_fuel_gauge_status_reg(self):
        response = self.i2c_read(0x64, 0x00, 1)
        if(response==None):
            return None
        data = response['data'][0]
        return data
    
    def get_fuel_gauge_voltage(self):
        response = self.i2c_read(0x64, 0x08, 1)
        if(response==None):
            return None
        data_msb = response['data'][0]
        response = self.i2c_read(0x64, 0x09, 1)
        if(response==None):
            return None
        data_lsb = response['data'][0]
        data = data_msb << 8 | data_lsb
        return data
    
    def get_fuel_gauge_current(self):
        response = self.i2c_read(0x64, 0x0E, 1)
        if(response==None):
            return None
        data_msb = response['data'][0]
        response = self.i2c_read(0x64, 0x0F, 1)
        if(response==None):
            return None
        data_lsb = response['data'][0]
        data = data_msb << 8 | data_lsb
        return data
    
    def get_fuel_gauge_charge(self):
        response = self.i2c_read(0x64, 0x02, 1)
        if(response==None):
            return None
        data_msb = response['data'][0]
        response = self.i2c_read(0x64, 0x03, 1)
        if(response==None):
            return None
        data_lsb = response['data'][0]
        data = data_msb << 8 | data_lsb
        return data
    
    def get_fuel_gauge_temperature(self):
        response = self.i2c_read(0x64, 0x14, 1)
        if(response==None):
            return None
        data_msb = response['data'][0]
        response = self.i2c_read(0x64, 0x15, 1)
        if(response==None):
            return None
        data_lsb = response['data'][0]
        data = data_msb << 8 | data_lsb
        return data
    
    def set_image_flip(self, flip):
        response = self.fpga_write(0x43, flip)
            
    def set_global_offset_forced(self, data):
        addr = 0x2
        data = (data & 0xFFFF)
        self.set_sensor_param_athena(addr, data)
        
    def set_detector_bias(self, data):
        addr = 0x1
        data = (data & 0xFF)
        self.set_sensor_param_athena(addr, data)
    
    def set_heating_compensation(self, data):
        addr = 0x4
        data = (data & 0xFF)
        self.set_sensor_param_athena(addr, data)

    def set_temp_sense_offset(self, data):
        addr = 0x3
        data = (data & 0xF)
        self.set_sensor_param_athena(addr, data)
    
    def set_coarse_offset_dc(self, data):
        addr = 0x5
        data = (data & 0xFF)
        self.set_sensor_param_athena(addr, data)
        
    def set_sensor_gain(self, data):
        addr = 0x6
        data = ((data<<2) | 0x01)
        self.set_sensor_param_athena(addr, data)
        
    def set_intergration_time_start(self, data):
        addr = 0xc
        data = data & 0x3FF
        self.set_sensor_param_athena(addr, data)
        
    def set_store_line_num(self, data):
        # addr = 0x10*2+0x2
        addr = 9
        self.set_sensor_param_athena(addr, data)
        
    def set_avergae_coarse_gain(self, data):
        addr = 0x10*2+0x1
        self.set_sensor_param_athena(addr, data)
    
    def enable_coarse_offset(self):
        addr = 0x7
        data = 1
        self.set_sensor_param_athena(addr, data)
    
    def set_coarse_offset_base_address(self, data):
        addr = 0x8
        self.set_sensor_param_athena(addr, data)
        
        
    def disable_coarse_offset(self):
        addr = 0x7
        data = 0
        self.set_sensor_param_athena(addr, data)
    
    def start_coarse_offset_cal(self):
        addr = 0x10*2+0x0
        data = 1
        self.set_sensor_param_athena(addr, data)
    
    def use_updated_coarse_offset(self, data):
        addr = 0x10*2+0x4
        data = data & 0x1
        self.set_sensor_param_athena(addr, data)
        
    def use_flat_coarse_offset(self, data):
        addr = 0x10*2+0x4
        data = (data & 0x1) << 1;
        self.set_sensor_param_athena(addr, data)
        
    
    def lock_global_offset(self):
        addr = 0x0
        data = 0x1
        self.set_sensor_param_athena(addr, data)
    
    def auto_global_offset(self):
        addr = 0x0
        data = 0x0
        self.set_sensor_param_athena(addr, data)
    
    def force_global_offset(self):
        addr = 0x0
        data = 0x2
        self.set_sensor_param_athena(addr, data)
    
    def enable_heating_monitor(self):
        addr = 11
        data = 1
        self.set_sensor_param_athena(addr, data)
        
    def disable_heating_monitor(self):
        addr = 11
        data = 0
        self.set_sensor_param_athena(addr, data)
    
    def set_image_min_value(self,data):
        addr = 0x10+10
        data = data & 0x3FFF
        self.set_sensor_param_athena(addr, data)
    
    def set_image_max_value(self,data):
        addr = 0x10+11
        data = data & 0x3FFF
        self.set_sensor_param_athena(addr, data)
    
    def get_image_min_value(self):
        addr = 0x10+10
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                image_min_value = (response['data'][-2]<<8) | response['data'][-1]
                return image_min_value
            except:
                return -1
        return -1
    
    def get_store_line_num(self):
        addr = 9
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                line_num = (response['data'][-2]<<8) | response['data'][-1]
                return line_num
            except:
                return -1
        return -1

    def get_intergration_time_start(self):
        addr = 0xc
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                sensor_integration_time = (response['data'][-2]<<8) | response['data'][-1]
                return sensor_integration_time
            except:
                return -1
        return -1

    def get_image_max_value(self):
        addr = 0x10+11
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                image_max_value = (response['data'][-2]<<8) | response['data'][-1]
                return image_max_value
            except:
                return -1
        return -1
    
        
    def get_detector_bias(self):
        addr = 0x1
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                detector_bias = response['data'][-1]
                return detector_bias
            except:
                return -1
        return -1
    
    def get_global_offset_forced(self):
        addr = 0x2
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                global_offset = (response['data'][-2]<<8) | response['data'][-1]
                return global_offset
            except:
                return -1
        return -1
    
    def get_global_offset(self):
        addr = 0xA
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                global_offset = (response['data'][-2]<<8) | response['data'][-1]
                return global_offset
            except:
                return -1
        return -1
        
    def get_heating_compensation(self):
        addr = 0x4
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                heating_compensation = response['data'][-1]
                return heating_compensation
            except:
                return -1
        return -1
    
    def get_temp_sense_offset(self):
        addr = 0x3
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try: 
                temp_sense_offset = response['data'][-1]
                return temp_sense_offset
            except:
                return -1
        return -1
    
    def get_override_sensor_param(self):
        addr = 0x0
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                override_sensor_param = response['data'][-1]
                return override_sensor_param
            except:
                return -1
        return -1
    
    def get_coarse_offset_dc(self):
        addr = 0x10*2+0x3
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                coarse_offset_dc = response['data'][-1]
                return coarse_offset_dc
            except:
                return -1
        return -1

    def get_sensor_gain(self):
        addr = 0x6
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                sensor_gain = response['data'][-1]
                return sensor_gain >> 2
            except:
                return -1
        return -1
    
    def enable_blind_pix_subtraction(self):
        addr = 0x10
        data = 0x01
        self.set_sensor_param_athena(addr, data)
    
    def disable_blind_pix_subtraction(self):
        addr = 0x10
        data = 0x00
        self.set_sensor_param_athena(addr, data)
        
        
    def get_meta1_avg(self):
        addr = 0x11
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                meta1_avg = (response['data'][-2]<<8) | response['data'][-1]
                return meta1_avg
            except:
                return -1
        return -1
    
    def get_meta2_avg(self):
        addr = 0x12
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                meta2_avg = (response['data'][-2]<<8) | response['data'][-1]
                return meta2_avg
            except:
                return -1
        return -1
    
    def get_meta3_avg(self):
        addr = 0x13
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                meta3_avg = (response['data'][-2]<<8) | response['data'][-1]
                return meta3_avg
            except:
                return -1
        return -1
    
    def get_blind_pix_avg_frame(self):
        addr = 0x14
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                blind_pix_avg = (response['data'][-2]<<8) | response['data'][-1]
                return blind_pix_avg
            except:
                return -1
        return -1
    
    def get_blind_pix_avg_row(self):
        addr = 0x15
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                blind_pix_avg = (response['data'][-2]<<8) | response['data'][-1]
                return blind_pix_avg
            except:
                return -1
        return -1
    
    def get_img_avg(self):
        addr = 0x19
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                img_avg = (response['data'][-2]<<8) | response['data'][-1]
                return img_avg
            except:
                return -1
        return -1
        
    def get_dark_pixel_count(self):
        addr = 0x16
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                dark_pixel_count = (response['data'][-4]<<24) | (response['data'][-3]<<16) | (response['data'][-2]<<8) | response['data'][-1]
                return dark_pixel_count
            except:
                return -1
        return -1
    
    def get_saturated_pixel_count(self):
        addr = 0x17
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                saturated_pixel_count = (response['data'][-4]<<24) | (response['data'][-3]<<16) | (response['data'][-2]<<8) | response['data'][-1]
                return saturated_pixel_count
            except:
                return -1
        return -1
    
    def get_frame_pixel_count(self):
        addr = 0x18
        response = self.get_sensor_param_athena(addr)
        if(response!=None):
            try:
                frame_pixel_count = (response['data'][-4]<<24) | (response['data'][-3]<<16) | (response['data'][-2]<<8) | response['data'][-1]
                return frame_pixel_count
            except:
                return -1
        return -1
        
    def get_image_minmax(self):
        min_value, max_value = None, None
        response=self.fpga_read(0x69)
        if(response!=None):
            try:
                min_value = (response['data'][-2] << 8) | response['data'][-1]
            except:
                return -1, -1
        response=self.fpga_read(0x70)
        if(response!=None):
            try:
                max_value = (response['data'][-2] << 8) | response['data'][-1]
            except:
                return -1, -1
        if(min_value==None or max_value==None):
            return -1, -1
        else:
            return min_value, max_value
    
    def get_image_average(self):
        average = None
        response = self.fpga_read(0x93)
        if(response!=None):
            try:
                average=(response['data'][-2]<<8 | response['data'][-1])                
                if(average==None):
                    return -1
                else:
                    return average
            except:
                return -1
        return -1
                
    def get_image_average_raw(self):
        average = None
        response = self.fpga_read(0x71)
        if(response!=None):
            try:
                average=(response['data'][-2]<<8 | response['data'][-1])
                if(average==None):
                    return -1
                else:
                    return average
            except: 
                return -1
        return -1
    
    def get_device_serial_num(self):
        serial_num = None
        response = self.fpga_read(0xD6)
        if(response!=None):
            try:
                if(response!=None):
                    serial_num=(response['data'][-4]<<24 | response['data'][-3]<<16 |\
                                response['data'][-2]<<8 | response['data'][-1])
                    return serial_num
                else:
                    return -1
            except:
                return -1
        return -1
            
    def get_device_serial_num_new(self):
        serial_num1 = None
        serial_num2 = None
        response = self.fpga_read(0xD5)
        if(response!=None):
            try:
                serial_num1=(response['data'][-4]<<24 | response['data'][-3]<<16 |\
                            response['data'][-2]<<8 | response['data'][-1])
            except:
                return -1
        else:
            return -1
        
        response = self.fpga_read(0xD6)
        if(response!=None):
            try:
                serial_num2=(response['data'][-4]<<24 | response['data'][-3]<<16 |\
                            response['data'][-2]<<8 | response['data'][-1])
            except:
                return -1
        else:
            return -1
        
        serial_num = ((serial_num2 & 0xFF) << 24) | (serial_num1 & 0x00FFFFFF)
        return serial_num
        
    def init_temp_sensor(self):
        #HDC2010 output data rate select
        self.i2c_write(0x40, 0x0E, [0x54])
        #HDC2010 interrupt mask
        self.i2c_write(0x40, 0x07, [0x80])
        #HDC2010 Measurement config
        self.i2c_write(0x40, 0xf, [0x03])
    
    def get_temp_sensor_data(self):
        
        try:
            # Read LSB
            value1 = self.i2c_read(0x40, 0x00, 1)
            #read MSB
            value2 = self.i2c_read(0x40, 0x01, 1)
            value = (value2['data'][-1] <<8) | value1['data'][-1]
            #The following values were inferred from experiments
            value_temp = ((value*165)/2**16) - 40 -18            
            return value, value_temp
        
        except:
            return -1

    def shutter_close(self):
        shutter_dev_addr = 0x52
        reg_addr = 23
        data = [0x01, 0x00]
        response = self.i2c_write_16b(shutter_dev_addr, reg_addr, data)
        if(response==None):
            print('Shutter close failed, please try again')
            
    def shutter_open(self):
        shutter_dev_addr = 0x52
        reg_addr = 23
        data = [0x00, 0x00]
        response = self.i2c_write_16b(shutter_dev_addr, reg_addr, data)
        if(response==None):
            print('Shutter open failed, please try again')
        
    def set_num_image_for_avg(self, value):
        if(value>6):
            value=6
        self.fpga_write(0x92, value)    
    
    def assign_serial_num(self, value):
        self.fpga_write(0xD5, value)
        
    def assign_serial_num_new(self, value):
        self.fpga_write(0xD5, (value & 0x00FFFFFF))
        self.fpga_write(0xD6, (value & 0xFF000000) >> 24)
        

    def perform_nuc1pt(self, img_avg=3):
        self.set_num_image_for_avg(img_avg)
        self.fpga_write(0x91, 1)
        self.fpga_write(0x91, 0)

    def perform_nuc1pt_apply(self, unity_gain=0):
        self.perform_nuc1pt()
        self.fpga_write(0x91, 2)
        if(unity_gain==1):
            self.fpga_write(0x54, 3)        

    def get_sensor_temp_raw(self):
        temp = None
        response = self.fpga_read(0x41)
        if(response!=None):
            temp = (response['data'][-2] << 8) | response['data'][-1]
            return temp
        return -1

    def get_temp_area(self):
        temp = None
        response = self.fpga_read(0x74)
        if(response!=None):
            try:
                temp = (response['data'][-2] << 8) | response['data'][-1]
                return temp
            except:
                return -1
        return -1
    
    def get_device_firmware_version(self):
        serial_num = None
        response = self.fpga_read(0x10)
        if(response!=None):
            try:
                serial_num=(response['data'][-4]<<24 | response['data'][-3]<<16 |\
                            response['data'][-2]<<8 | response['data'][-1])
                return serial_num
            except:
                return -1
        else:
            return -1

    def switch_temp_area(self, value):
        if(value==0):
            self.fpga_write(0x97, 4)    
        elif(value==1):
            self.fpga_write(0x97, 5)
        elif(value==2):
            self.fpga_write(0x97, 6)
        elif(value==3):
            self.fpga_write(0x97, 7)
        else:
            self.logger.info('Illegal temperature area')
    
    def switch_athena_temp_area(self, value):
        self.fpga_write(0x97, 8+value)
        
    
    def switch_CO_bus_mode(self, value):
        self.fpga_write(0x9B, value & 0xF)
    
    def set_CO_mode(self, value):
        self.fpga_write(0x9C, value & 0xF)
    
    def trigger_wait_CO_calc(self):
        self.fpga_write(0x98,0x1)
        #wait for 1 second to finish the calculations
        time.sleep(1)

    def set_CO_addr(self, addr):
        self.fpga_write(0x9A, addr)
    
    def set_CO_dc_val(self, val):
        self.fpga_write(0x9d, val & 0xFF)
    
    def erase_qspi(self, address, size):
        
        '''
        erase_qspi method takes qspi address and the total size to
        be erased and splits them in chunks of 4KB, 32KB and 64KB erase
        commands as defined by the Micron QSPI Flash
        
        Splitting works as progressively tries to find the next best 
        4K, 32K or 64K boundary and then applying the QSPI commands
        '''
        if(size%0x1000!=0):
            print('size not a multiple of 4KB')
            return
        
        qspi_start_address = address
        qspi_end_address = address + size
        
        print('qspi_address = %x'%qspi_start_address)
        while(qspi_start_address<qspi_end_address):
            boundary = qspi_start_address & 0x0000FFFF
            ##64K Boundary
            if(boundary==0):
                num_blocks_64k_erase = (qspi_end_address - qspi_start_address)>>16
                if(num_blocks_64k_erase>0):
                    self.erase_qspi_64KB(qspi_start_address, num_blocks_64k_erase)
                    ret = self.qspi_success_status(sleeptime_max=num_blocks_64k_erase*100)
                    if(ret==0):
                        print('Erase success')
                    else:
                        print('Unsuccessful, returning')
                        return -1
                        
                    qspi_start_address += num_blocks_64k_erase*0x10000
                    print('64K Blocks %d'%num_blocks_64k_erase)
                    print('qspi_address = %x'%qspi_start_address)
                else:
                    num_blocks_32k_erase = (qspi_end_address - qspi_start_address)>>15
                    if(num_blocks_32k_erase>0):
                        self.erase_qspi_32KB(qspi_start_address, num_blocks_32k_erase)
                        ret = self.qspi_success_status(sleeptime_max=num_blocks_32k_erase*100)
                        if(ret==0):
                            print('Erase success')
                        else:
                            print('Unsuccessful, returning')
                            return -1
                        qspi_start_address += num_blocks_32k_erase*0x8000
                        print('32K Blocks %d'%num_blocks_32k_erase)
                        print('qspi_address = %x'%qspi_start_address)
                    else:
                        num_blocks_4k_erase = (qspi_end_address - qspi_start_address)>>12
                        self.erase_qspi_4KB(qspi_start_address, num_blocks_4k_erase)
                        ret = self.qspi_success_status(sleeptime_max=num_blocks_4k_erase*100)
                        if(ret==0):
                            print('Erase success')
                        else:
                            print('Unsuccessful, returning')
                            return -1
                        qspi_start_address += num_blocks_4k_erase*0x1000
                        print('4K Blocks %d'%num_blocks_4k_erase)
                        print('qspi_address = %x'%qspi_start_address)
            #32K boundary        
            elif(boundary==0x8000):
                num_blocks_32k_erase = (qspi_end_address - qspi_start_address)>>15
                if(num_blocks_32k_erase>0):
                    self.erase_qspi_32KB(qspi_start_address, 1)
                    ret = self.qspi_success_status(sleeptime_max=1*100)
                    if(ret==0):
                        print('Erase success')
                    else:
                        print('Unsuccessful, returning')
                        return -1
                    qspi_start_address += 1*0x8000
                    print('32K Blocks 1')
                    print('qspi_address = %x'%qspi_start_address)
                else:
                    num_blocks_4k_erase = ((qspi_end_address - qspi_start_address)>>12)
                    self.erase_qspi_4KB(qspi_start_address, num_blocks_4k_erase)
                    ret = self.qspi_success_status(sleeptime_max=num_blocks_4k_erase*100)
                    if(ret==0):
                        print('Erase success')
                    else:
                        print('Unsuccessful, returning')
                        return -1
                    qspi_start_address += num_blocks_4k_erase*0x1000
                    print('4K Blocks %d'%num_blocks_4k_erase)
                    print('qspi_address = %x'%qspi_start_address)
            #4K boundary        
            elif((boundary & 0x0FFF)==0):
                num_blocks_4k_erase = ((qspi_end_address - qspi_start_address)>>12)
                #check if blocks are greater than 32K
                if(num_blocks_4k_erase>=8):
                    num_blocks = (((qspi_start_address & 0xFFFF0000)+0x8000) - qspi_start_address)>>12
                    #check if the next aligned address is below 32K boundary or above
                    if(num_blocks>0):
                        self.erase_qspi_4KB(qspi_start_address, num_blocks)
                        ret = self.qspi_success_status(sleeptime_max=num_blocks*100)
                        if(ret==0):
                            print('Erase success')
                        else:
                            print('Unsuccessful, returning')
                            return -1
                        qspi_start_address += num_blocks*0x1000
                        print('4K Blocks %d'%num_blocks)
                        print('qspi_address = %x'%qspi_start_address)
                    #if below 32K boundary check if blocks are greater than 64K    
                    elif(num_blocks_4k_erase>=16):
                        num_blocks = (((qspi_start_address & 0xFFFF0000)+0x10000) - qspi_start_address)>>12
                        self.erase_qspi_4KB(qspi_start_address, num_blocks)
                        ret = self.qspi_success_status(sleeptime_max=num_blocks*100)
                        if(ret==0):
                            print('Erase success')
                        else:
                            print('Unsuccessful, returning')
                            return -1
                        qspi_start_address += num_blocks*0x1000
                        print('4K Blocks %d'%num_blocks)
                        print('qspi_address = %x'%qspi_start_address)
                    else:
                        self.erase_qspi_4KB(qspi_start_address, num_blocks_4k_erase)
                        ret = self.qspi_success_status(sleeptime_max=num_blocks_4k_erase*100)
                        if(ret==0):
                            print('Erase success')
                        else:
                            print('Unsuccessful, returning')
                            return -1
                        qspi_start_address += num_blocks_4k_erase*0x1000
                        print('4K Blocks %d'%num_blocks_4k_erase)
                        print('qspi_address = %x'%qspi_start_address)
                else:
                    self.erase_qspi_4KB(qspi_start_address, num_blocks_4k_erase)
                    ret = self.qspi_success_status(sleeptime_max=num_blocks_4k_erase*100)
                    if(ret==0):
                        print('Erase success')
                    else:
                        print('Unsuccessful, returning')
                        return -1
                    qspi_start_address += num_blocks_4k_erase*0x1000
                    print('4K Blocks %d'%num_blocks_4k_erase)
                    print('qspi_address = %x'%qspi_start_address)
            

    def qspi_success_status(self, sleeptime_max=50):
        unsuccessful = True
        sleeptime = 0
        while(unsuccessful):
            unsuccessful = False
            response=self.get_qspi_status()
            for i in range(response['length']-4-3):
                if(response['data'][i]!=0):
                    unsuccessful = True
            if(unsuccessful==False):
                break
            time.sleep(0.1)
            sleeptime += 10
            if(sleeptime>sleeptime_max):
                unsuccessful = True
                break

        if(unsuccessful==False):
            return 0
        else:
            return -1
        
    def take_snapshot(self, channel=0, mode=0, number_frames=32):

        retries = 0
        response = self.perform_snapshot(channel=channel, mode=mode, number_frames=number_frames) 
        if(mode==3 or mode>=8):
            return
        if(response!=None):
            if(mode!=4):
                time.sleep(number_frames//2)
            while(1):
                if(mode==4):
                    sleeptime = 200
                else:
                    sleeptime = 1000
                ret =  self.qspi_success_status(sleeptime_max=sleeptime)
#                print('Return value = %d'%ret)
                if(ret==0):
                    print('Successfully stored snapshots in QSPI Flash') 
                    break
                else:
                    retries = retries+1
                    if(retries==5):
                        print('Could not save images in QSPI Flash')
                        break
 
    def save_offset_table(self, table):

        if(table<0 or table>59):    
            self.logger.info('Illegal table number')
        else:
            self.erase_save_table(table)
            ret=self.qspi_success_status(sleeptime_max=200)
            if(ret==-1):
                self.logger.info('Warning, something wrong with qspi')
    
    def capture_save_offset_table(self, table):
        self.perform_nuc1pt_apply()
        time.sleep(3)
        self.save_offset_table(table)
    
    def capture_save_frame(self, table):
        self.set_num_image_for_avg(0)
        self.fpga_write(0x91, 1)
        self.fpga_write(0x91, 0)
        time.sleep(3)
        self.save_offset_table(table)
        
    def save_sensor_param_area(self, value):
        if(value==0):
            self.sensor_init_temp_area0_save()
        elif(value==1):
            self.sensor_init_temp_area1_save()
        elif(value==2):
            self.sensor_init_temp_area2_save()
        elif(value==3):
            self.sensor_init_temp_area3_save()
        else:
            self.logger.info('Illegal area value')
            return
        ret=self.qspi_success_status()
        if(ret==-1):
            self.logger.info('Warning, something wrong with qspi')
    
    def save_athena_sensor_param_area(self, value):
        self.sensor_init_temp_area_save(value)
        ret = self.qspi_success_status()
        if(ret==-1):
            self.logger.info('Warning, something wrong with qspi')

    def save_cold_image(self):
        self.erase_save_table(0x00080000)
        time.sleep(2)
        ret=self.qspi_success_status()
        if(ret==-1):
            self.logger.info('Warning, something wrong with qspi')

    def save_hot_image(self):
        self.erase_save_table(0x00080001)
        time.sleep(2)
        ret=self.qspi_success_status()
        if(ret==-1):
            self.logger.info('Warning, something wrong with qspi')

    def capture_image_avg(self, value=3):
        self.set_num_image_for_avg(value)
        self.fpga_write(0x91, 0x5)        
        self.fpga_write(0x91, 0x0)

    def capture_save_cold_image(self):
        self.fpga_write(0x95,0x0)
        self.capture_image_avg()
        self.save_cold_image()

    def capture_save_hot_image(self):
        self.fpga_write(0x95,0x1)
        self.capture_image_avg()
        self.save_hot_image()

    def start_gain_calc(self):
        self.fpga_write(0x96, 1)
        self.fpga_write(0x96, 0)

    def select_current_gain_table(self):
        self.fpga_write(0x94, 1)

    def save_gain(self):
        self.erase_save_table(0x000f0001)
        time.sleep(1)
        ret=self.qspi_success_status()
        if(ret==-1):
            self.logger.info('Warning, something wrong with qspi')
    
    def get_heating_monitor_data(self, memory_address=0x2000000):
        heating_monitor_array = [0]*519
        #enable heating monitor
        # print('Meta 3 avg (Before heating monitor) = %d'%self.get_meta3_avg())
        self.enable_heating_monitor()
        #take snapshot
        self.take_snapshot(channel=0, mode=12, number_frames=1)
        
        # print('Meta 3 avg (After heating monitor) = %d'%self.get_meta3_avg())
        #disable heating monitor
        self.disable_heating_monitor()
        #take the column 3 values and store it in a array
        address = memory_address+2*2
        for i in range(519):
            self.set_sdram_addr(address);
            response = self.get_sdram_data(4); #get value stored in column
            value = (response['data'][-2] << 8) | response['data'][-1]
            heating_monitor_array[i] = value
            address = address+664*2
            time.sleep(0.1)
            
        return heating_monitor_array

    def get_heating_monitor_data_fast_mode(self, memory_address=0x2000000):
        heating_monitor_array = [0]*519
        #enable heating monitor
        # print('Meta 3 avg (Before heating monitor) = %d'%self.get_meta3_avg())
        self.enable_heating_monitor()
        #take snapshot
        self.take_snapshot(channel=0, mode=12, number_frames=1)
        
        # print('Meta 3 avg (After heating monitor) = %d'%self.get_meta3_avg())
        #disable heating monitor
        self.disable_heating_monitor()
        #take the column 3 values and store it in a array
        address = memory_address+2*2
        for i in range(519):
            if(i>39 and i<321):
                self.set_sdram_addr(address);
                response = self.get_sdram_data(4); #get value stored in column
                value = (response['data'][-2] << 8) | response['data'][-1]
                heating_monitor_array[i] = value
                # address = address+664*2
                # time.sleep(0.1)
            else:
                 heating_monitor_array[i] = 8192
            address = address+664*2
        return heating_monitor_array
        
    def store_reticle(self, address, reticle_img):
        reticle_img_len = len(reticle_img)
        #Send 240 bytes at once
        x = reticle_img_len//240

        for i in range(x):
            self.printProgressBar(i,x)
            response=self.set_sdram_addr(address)
            response=self.set_sdram_data2(reticle_img[i*240:(i+1)*240])
            #increment address by 240
            address = address+240
    
    
    def read_data_sdram(self, address, size):
        if(size%4!=0):
            print('Size not a multiple of 4')
            return
        size_ = size
        address_ = address
        data = []
        
        while(size_>0):
            self.printProgressBar((size-size_), size)
            if(size_>240):
                self.set_sdram_addr(address_)
                response=self.get_sdram_data(240)
                data.extend(response['data'])
                size_ -=240
                address_+=240
            else:
                self.set_sdram_addr(address_)
                response=self.get_sdram_data(size_)
                data.extend(response['data'])
                address_+=size_
                size_ = 0
        
        return data
                
    # Print iterations progress
    def printProgressBar (self, iteration_val, total_val, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration_val / float(total_val)))
        filledLength = int(length * iteration_val // total_val)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration_val == total_val-1: 
            print('\n')
             
    def offset_calib(self, temp):
        response = self.ping(5)
        if(response==None):
            self.logger.info('Ping failed, check communication link of device')
            return -1

        t_area = []
        
        t_area.append({-40:1, -30:2, -20:3, -15:4, -10:5, -5:6,\
                      0:7, 5:8, 10:9, 12:10, 14:11})
        
        t_area.append({10:12, 12:13, 14:14, 16:15, 18:16, 20:17, 22:18,\
                    24:19, 26:20, 28:21, 30:22, 32:23, 34:24, 36:25})
        
        t_area.append({32:26, 34:27, 36:28, 38:29, 40:30, 42:31, 44:32,\
                    46:33, 48:34, 50:35, 52:36, 54:37, 56:38})
        
        t_area.append({52:39, 54:40, 56:41, 58:42, 60:43, 62:44, 65:45 })
        
        if((temp not in t_area[0]) and (temp not in t_area[1])\
           and (temp not in t_area[2]) and (temp not in t_area[3])):
            self.logger.info('Critical temperature incorrect/out of range')
            return -1
        if(temp in t_area[0]):
            table = t_area[0][temp]
            self.logger.info('Switching to temp area0')
            self.switch_temp_area(0)
            if(temp in t_area[1]):
                time.sleep(2*60)
            self.logger.info('Disabling NUC')
            self.disable_nuc()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values')
            min_value1,max_value1 = self.get_image_minmax()
            self.logger.info('Enabling NUC')
            self.enable_nuc()
            time.sleep(3)
            self.logger.info('Capturing and Saving offset')
            self.capture_save_offset_table(table)
            tmp = self.get_sensor_temp_raw()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values again')
            min_value2, max_value2 = self.get_image_minmax()
            
            with open('calib_log_'+self.dev_name+'.log', 'a') as f:
                f.write('Table Number: %d\n'%(table))
                f.write('RAW:Image Min=%d, Max=%d\n'%(min_value1, max_value1))
                f.write('Sensor temperature=%d\n'%(tmp))
                f.write('NUC:Image Min=%d, Max=%d\n'%(min_value2, max_value2))
                f.write('\n\n')
            
        if(temp in t_area[1]):
            table = t_area[1][temp]
            self.logger.info('Switching to temp area1')
            self.switch_temp_area(1)
            if((temp in t_area[0]) or(temp in t_area[2])):
                time.sleep(2*60)
            self.logger.info('Disabling NUC')
            self.disable_nuc()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values')
            min_value1,max_value1 = self.get_image_minmax()
            self.logger.info('Enabling NUC')
            self.enable_nuc()
            time.sleep(3)
            self.logger.info('Capturing and Saving offset')
            self.capture_save_offset_table(table)
            tmp = self.get_sensor_temp_raw()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values again')
            min_value2, max_value2 = self.get_image_minmax()
            
            with open('calib_log_'+self.dev_name+'.log', 'a') as f:
                f.write('Table Number: %d\n'%(table))
                f.write('RAW:Image Min=%d, Max=%d\n'%(min_value1, max_value1))
                f.write('Sensor temperature=%d\n'%(tmp))
                f.write('NUC:Image Min=%d, Max=%d\n'%(min_value2, max_value2))
                f.write('\n\n')

        if(temp in t_area[2]):
            table = t_area[2][temp]
            self.logger.info('Switching to temp area2')
            self.switch_temp_area(2)
            if((temp in t_area[1]) or (temp in t_area[3]) ):
                time.sleep(2*60)
            self.logger.info('Disabling NUC')
            self.disable_nuc()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values')
            min_value1,max_value1 = self.get_image_minmax()
            self.logger.info('Enabling NUC')
            self.enable_nuc()
            time.sleep(3)
            self.logger.info('Capturing and Saving offset')
            self.capture_save_offset_table(table)
            tmp = self.get_sensor_temp_raw()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values again')
            min_value2, max_value2 = self.get_image_minmax()
            
            with open('calib_log_'+self.dev_name+'.log', 'a') as f:
                f.write('Table Number: %d\n'%(table))
                f.write('RAW:Image Min=%d, Max=%d\n'%(min_value1, max_value1))
                f.write('Sensor temperature=%d\n'%(tmp))
                f.write('NUC:Image Min=%d, Max=%d\n'%(min_value2, max_value2))
                f.write('\n\n')
 
        if(temp in t_area[3]):
            table = t_area[3][temp]
            self.logger.info('Switching to temp area3')
            self.switch_temp_area(3)
            if(temp in t_area[2]) :
                time.sleep(2*60)
            self.logger.info('Disabling NUC')
            self.disable_nuc()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values')
            min_value1,max_value1 = self.get_image_minmax()
            self.logger.info('Enabling NUC')
            self.enable_nuc()
            time.sleep(3)
            self.logger.info('Capturing and Saving offset')
            self.capture_save_offset_table(table)
            tmp = self.get_sensor_temp_raw()
            time.sleep(3)
            self.logger.info('Getting IMG min and max values again')
            min_value2, max_value2 = self.get_image_minmax()
            
            with open('calib_log_'+self.dev_name+'.log', 'a') as f:
                f.write('Table Number: %d\n'%(table))
                f.write('RAW:Image Min=%d, Max=%d\n'%(min_value1, max_value1))
                f.write('Sensor temperature=%d\n'%(tmp))
                f.write('NUC:Image Min=%d, Max=%d\n'%(min_value2, max_value2))
                f.write('\n\n') 
        return 0

if __name__ == "__main__":
    
    # com_file = open("com_num.txt", "r")
    COM_PORT = "COM10"
    print("COM PORT = ",COM_PORT)
    
    ser = serial.Serial(COM_PORT, 115200, timeout=5)
    cmd_gen = SensorComm(ser, dev_name='pico640', idd='new')
    print(cmd_gen.ping_device())
    print(cmd_gen.get_meta1_avg())
    ser.close()