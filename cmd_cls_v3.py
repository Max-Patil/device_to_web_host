import random as rn
import serial
import time
import logging
import sys

logger_d = logging.getLogger(__name__)

cmd_log_file = "./cmd_log.txt"

class CMD:
    def __init__(self, ser=None, dev_name=None, idd='old'):
        self.ser = ser
        self.idd = idd
        self.sequence = 0
        self.mem_cmd_id = 0
        self.mem_cmd_type = 0
        self.dev_name = dev_name
        self.logger = logger_d
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(logging.DEBUG)
        self.logger.addHandler(consoleHandler)
        
        if(self.idd=='new'):
            self.init_cmd_new_idd()
        else:
            self.init_cmd_old_idd()
    
    def __del__(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
            del handler
        logging.shutdown()
        

    def init_cmd_old_idd(self):
        self.PING_CMD = 0xB0B0
        self.FPGA_RD_REGS = 0x4000
        self.FPGA_WR_REGS = 0x5000
        self.SET_SDRAM_ADDR = 0x6000
        self.SET_SDRAM_DATA = 0x6004
        self.GET_SDRAM_DATA = 0x6008
        self.SET_I2C = 0x7004
        self.GET_I2C = 0x7008
        self.SET_SENSOR_I2C = 0x7104
        self.GET_SENSOR_I2C = 0x7108
        self.SET_SPI = 0x3004
        self.GET_SPI = 0x3008
        self.SET_SD_ADDR = 0x2000
        self.SET_SD_DATA = 0x2004
        self.GET_SD_DATA = 0x2008
        self.ERASE_QSPI_64KB = 0xA000
        self.ERASE_QSPI_32KB = 0xA001
        self.ERASE_QSPI_4KB  = 0xA002
        self.ERASE_SAVE_QSPI = 0xA004
        self.SNAPSHOT = 0xA00E
        self.TRANS_SDRAM_TO_QSPI = 0xA003
        self.TRANS_QSPI_TO_SDRAM = 0xE000
        self.QSPI_STATUS_CMD     = 0xA008
        self.TRANS_TEMP_TO_QSPI = 0xE00C
        self.TEMP_RANGE0_SENSOR_INIT_WR_QSPI = 0xE00D
        self.TEMP_RANGE1_SENSOR_INIT_WR_QSPI = 0xE00E
        self.TEMP_RANGE2_SENSOR_INIT_WR_QSPI = 0xE00F
        self.TEMP_RANGE3_SENSOR_INIT_WR_QSPI = 0xE010

        
        self.BLK_SIZE= 512
        self.header = 0xFE
        self.dev_id = 0x3E
        self.dev_no =  0xFF
        

    def init_cmd_new_idd(self):
        self.PING_CMD = 0xB0B0
        self.FPGA_RD_REGS = 0x5000
        self.FPGA_WR_REGS = 0x5000
        self.SET_SDRAM_ADDR = 0x6000
        self.SET_SDRAM_DATA = 0x6004
        self.GET_SDRAM_DATA = 0x6004
        self.SET_I2C = 0x7004
        self.GET_I2C = 0x7004
        self.SET_I2C_16B = 0x7005
        self.GET_I2C_16B = 0x7005
        self.SET_SENSOR_I2C = 0x7104
        self.GET_SENSOR_I2C = 0x7104
        self.SET_SPI = 0x3004
        self.GET_SPI = 0x3004
        self.SET_SD_ADDR = 0x2000
        self.SET_SD_DATA = 0x2004
        self.GET_SD_DATA = 0x2004
        self.ERASE_SAVE_TABLE = 0xA004
        self.ERASE_QSPI_64KB = 0xA000
        self.ERASE_QSPI_32KB = 0xA001
        self.ERASE_QSPI_4KB  = 0xA002
        self.ERASE_SAVE_QSPI = 0xA004
        self.SNAPSHOT = 0xA00E
        self.TRANS_SDRAM_TO_QSPI = 0xA003
        self.TRANS_QSPI_TO_SDRAM = 0xE000
        self.QSPI_STATUS_CMD     = 0xA008
        self.TRANS_TEMP_TO_QSPI  = 0xE00C
        self.SAVE_USER_SETTINGS  = 0xA005
        self.TEMP_RANGE0_SENSOR_INIT_WR_QSPI = 0xE00D
        self.TEMP_RANGE1_SENSOR_INIT_WR_QSPI = 0xE00E
        self.TEMP_RANGE2_SENSOR_INIT_WR_QSPI = 0xE00F
        self.TEMP_RANGE3_SENSOR_INIT_WR_QSPI = 0xE010
        self.TEMP_RANGE4_SENSOR_INIT_WR_QSPI = 0xE011
        self.TEMP_RANGE5_SENSOR_INIT_WR_QSPI = 0xE012
        self.TEMP_RANGE6_SENSOR_INIT_WR_QSPI = 0xE013
        
        
        self.BLK_SIZE= 512
        self.header = 0xE0
        self.response_header = 0xE1
        self.dev_id = 0x3E
        self.dev_no = 0xFF    
        self.footer1 = 0xFF
        self.footer2 = 0xFE   
        
        self.last_cmd = []
    
    def set_port(self, ser_port):
        self.ser = ser_port
    
    def set_devname(self, dev_name):
        self.dev_name = dev_name
        self.fileHandler.close()
        self.logger.removeHandler(self.fileHandler)
        fileHandler = logging.FileHandler('cmd_log_'+self.dev_name+'.log')
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.DEBUG)
        self.logger.addHandler(fileHandler)
        
    def write_packet(self, cmd):
        if(self.ser!=None): 
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytearray(cmd))
            print("Command : ",[hex(i) for i in cmd])
            self.last_cmd = cmd
            with open(cmd_log_file, 'a+') as f:
                f.write('\n COMND : \t')
                for byte in cmd:
                    f.write(hex(byte) + ", ")

    def read_packet(self):
        
        rt_cnt  = 0
        rt_max  = 10 
        
        rd_header   = 0
        rd_sequence = 0
        rd_dev_id   = 0
        rd_dev_num  = 0
        rd_length   = 0
        rd_cmd_id   = 0
        rd_cmd_type = 0
        
        if(self.ser==None):
            return 
        
        rd_cmd0 = bytearray (self.ser.read(5)) 
        if(len(rd_cmd0)!=5):
            return -1, None 

        while(1):
            
            if(rt_cnt > rt_max): # return if max number of tries over
                return -1, None 
            
            rd_header   = rd_cmd0[0]
            rd_sequence = rd_cmd0[2] + (rd_cmd0[1] << 8)
            rd_dev_id   = rd_cmd0[3]
            rd_dev_num  = rd_cmd0[4]
            
            # rd_sequence = 10
                        
            if(rd_header == self.response_header\
               and rd_sequence == self.sequence\
               and rd_dev_id   == self.dev_id\
               and rd_dev_num  == self.dev_no ):
                
                break
            
            print("\n\nRESPONSE  : ", [hex(i) for i in rd_cmd0])
            
            print("\nRECEIVED HEADER")
            print("rd_header   : ",hex(rd_header))
            print("rd_sequence : ",hex(rd_sequence))
            print("rd_dev_id   : ",hex(rd_dev_id))
            print("rd_dev_name : ",hex(rd_dev_num))
            
            print("\nEXPECTED Header")
            print("rd_header   : ",hex(self.response_header))
            print("rd_sequence : ",hex(self.sequence))
            print("rd_dev_id   : ",hex(self.dev_id))
            print("rd_dev_name : ",hex(self.dev_no ))
            
            rd_cmd1 = self.ser.read(1) 
            if(len(rd_cmd1)!=1):
                return -1, None # return if buffer dosnt have any data
                    
            temp_rrd_cmd0 = rd_cmd0
            rd_cmd0 = temp_rrd_cmd0[1:] + rd_cmd1
            
            rt_cnt = rt_cnt +1
         
        rd_cmd2 = self.ser.read(1) 
        if(len(rd_cmd2) != 1):
            return -1, None 
        
        rd_length = rd_cmd2[0]
        
        expected_bytes_avail = rd_length+3
        rd_cmd3 = self.ser.read(expected_bytes_avail)
        
        if(len(rd_cmd3) != expected_bytes_avail):
            return -1, None
        
        rd_csm     = rd_cmd3[-3]
        rd_footer1 = rd_cmd3[-2]
        rd_footer2 = rd_cmd3[-1]
        
        rd_cmd_type  = rd_cmd3[0]
        rd_cmd_id    = rd_cmd3[3] + (rd_cmd3[2] << 8)  

        crc = 0
        crc = crc + rd_dev_id + rd_dev_num + rd_length
        for data in rd_cmd3 [0: -3]:            
            crc = crc + data
        crc = crc%256
        
        response = rd_cmd0 + rd_cmd2 + rd_cmd3
        with open(cmd_log_file, 'a+') as f:
            f.write('\n REPLY : \t')
            for byte in response:
                f.write(hex(byte) + ", ")

        if(rd_csm == crc\
           and rd_footer1  == self.footer1\
           and rd_footer2  == self.footer2\
           and rd_cmd_id   == self.mem_cmd_id\
           and rd_cmd_type == self.mem_cmd_type):
            
            print("response : ", [hex(i) for i in rd_cmd0 + rd_cmd2 + rd_cmd3])
                        
            return 0, rd_cmd0 + rd_cmd2 + rd_cmd3
        print("\n\nCOMMAND SEND       : ", [hex(i) for i in self.last_cmd])
        print("COORUPTED RESPONSE  : ", [hex(i) for i in rd_cmd0 + rd_cmd2 + rd_cmd3])
        print("\nRECEIVED Footer ERROR ")       
        print("rd_cmd_id    : ",hex(rd_cmd_id))
        print("rd_cmd_type  : ",hex(rd_cmd_type))
        print("rd_csm       : ",hex(rd_csm))
        print("rd_footer1   : ",hex(rd_footer1))
        print("rd_footer2   : ",hex(rd_footer2))        
        print("\nEXPECTED Footer")        
        print("rd_cmd_id    : ",hex(self.mem_cmd_id)) 
        print("rd_cmd_type  : ",hex(self.mem_cmd_type))
        print("rd_csm       : ",hex(crc))
        print("rd_footer1   : ",hex(self.footer1))
        print("rd_footer2   : ",hex(self.footer2))
        
        with open(cmd_log_file, 'a+') as f:
            f.write("\n\nCOORUPTED RESPONSE  : ")
            f.write("\nRECEIVED Footer ERROR ")       
            f.write("\nrd_cmd_id    : "+str(hex(rd_cmd_id)))
            f.write("\nrd_cmd_type  : "+str(hex(rd_cmd_type)))
            f.write("\nrd_csm       : "+str(hex(rd_csm)))
            f.write("\nrd_footer1   : "+str(hex(rd_footer1)))
            f.write("\nrd_footer2   : "+str(hex(rd_footer2))) 
            
            f.write("\n\nEXPECTED Footer")        
            f.write("\nrd_cmd_id    : "+str(hex(self.mem_cmd_id))) 
            f.write("\nrd_cmd_type  : "+str(hex(self.mem_cmd_type)))
            f.write("\nrd_csm       : "+str(hex(crc)))
            f.write("\nrd_footer1   : "+str(hex(self.footer1)))
            f.write("\nrd_footer2   : "+str(hex(self.footer2)))
            f.write("\n")
        
        return -1, None
        
    def split_num(self, data, split_way=4, endian=0):
        l = []
        mask = 0xFF
        for i in range(split_way):
            l.append((data & (mask << (8*i))) >> (8*i))
        if(endian==0):
            return l[::-1]
        else:
            return l
        
    def send_receive_response(self, cmd, retry=2):
        for i in range(retry):            
            self.write_packet(cmd)
            self.logger.debug([hex(i) for i in cmd])            
            status, rd_cmd = self.read_packet()
       
            response = {}
            if(status==0):
                response['data'] = []
                if(self.idd=='old'):
                    response['header'] = rd_cmd[0]
                    response['packet_sequence'] = 0
                    response['device_id'] = rd_cmd[1]
                    response['device_number'] = rd_cmd[2]
                    response['cmd_type'] = 0x57
                    response['cmd'] = (rd_cmd[4] <<8 | rd_cmd[3])
                    if(response['cmd']==0xDEAD):
                        response['cmd_status'] = 1
                    else:
                        response['cmd_status'] = 0
                    response['length'] = (rd_cmd[6] <<8 | rd_cmd[5])
                    for i in range(response['length']):
                        response['data'].append(rd_cmd[i+7])
                    response['chksum'] = rd_cmd[response['length']+1]
                    response['footer1'] = 255
                    response['footer2'] = 255
                else:
                    response['header'] = rd_cmd[0]
                    response['packet_sequence'] = (rd_cmd[1]<<8 | rd_cmd[2])
                    response['device_id'] = rd_cmd[3]
                    response['device_number'] = rd_cmd[4]
                    response['length'] = rd_cmd[5]
                    response['cmd_type'] = rd_cmd[6]
                    response['cmd_status'] = rd_cmd[7]
                    response['cmd'] = (rd_cmd[8] <<8 | rd_cmd[9])
                    for i in range(response['length']-4):
                        response['data'].append(rd_cmd[i+10])
                    response['chksum'] = rd_cmd[-3]
                    response['footer1'] = rd_cmd[-2]
                    response['footer2'] = rd_cmd[-1]
               
                self.logger.debug([hex(i) for i in rd_cmd])
                return response 
            else:
                self.logger.warning('Read Unsuccessful')
                
        self.logger.critical('Communication Link seems to be broken')
        return None
     

    def con_cmd(self, cmd, cmd_type, length, data):
        
        pkt =[]
        pkt.append(self.header)
        self.sequence += 1
        self.mem_cmd_id = cmd
        self.mem_cmd_type = cmd_type
        
        if(self.idd=='old'):
            pkt.append(self.dev_id)
            pkt.append(self.dev_no)
            pkt.append(cmd & 0xFF)
            pkt.append(cmd>>8)
            pkt.append(length & 0xFF)
            pkt.append(length >> 8)
            if(length!=0):
                pkt.extend(data)
            
            crc = 0
            for i in range(len(pkt)-1):
                crc=crc+pkt[i+1]
            crc = crc%256
            crc = ~crc & 0xFF
            crc = (crc+1)%256
            return pkt+[crc]
        
        else:
            pkt.append((self.sequence >> 8) & 0xFF)
            pkt.append((self.sequence & 0xFF))
            pkt.append(self.dev_id)
            pkt.append(self.dev_no)
            pkt.append((length+3) & 0xFF)
            pkt.append(cmd_type)
            pkt.append(cmd>>8)
            pkt.append(cmd & 0xFF)
            if(length!=0):
                pkt.extend(data)
            
            crc = 0
            for i in range(len(pkt)-1-2):
                crc=crc+pkt[i+1+2]
            crc = crc%256
            return pkt+[crc, self.footer1, self.footer2]

    def ping(self, ping_length):
        self.logger.info('Sending PING command')
        cmd = self.PING_CMD
        cmd_type = 0x57
        length = ping_length
        data = [rn.randint(0,255) for x in range(ping_length)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def fpga_read(self, addr):
        self.logger.info('Reading FPGA register 0x%x'%(addr))
        cmd = self.FPGA_RD_REGS | (addr & 0xFFF)
        cmd_type = 0x52
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
        
    
    def fpga_write(self, addr, data):    
        self.logger.info('Writing to FPGA register, 0x%x=0x%x'%(addr,data))
        cmd = self.FPGA_WR_REGS | (addr & 0xFFF)
        cmd_type = 0x57
        length = 4
        if(self.idd=='new'):
            data = self.split_num(data,split_way=4, endian=0)
        else:
            data = self.split_num(data,split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def i2c_write(self, dev_addr, reg_addr, wr_data):
        self.logger.info('Writing I2C device 0x%x, reg 0x%x \
                         with data'%(dev_addr,reg_addr))
        self.logger.info([hex(i) for i in wr_data])
        cmd = self.SET_I2C
        cmd_type = 0x57
        length = 2+len(wr_data)
        data = [(dev_addr & 0xFF), (reg_addr & 0xFF)]
        data.extend([x for x in wr_data])
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
    
    def i2c_write_16b(self, dev_addr, reg_addr, wr_data):
        self.logger.info('Writing I2C device 0x%x, reg 0x%x \
                         with data'%(dev_addr,reg_addr))
        self.logger.info([hex(i) for i in wr_data])
        cmd = self.SET_I2C_16B
        cmd_type = 0x57
        length = 2+len(wr_data)
        data = [(dev_addr & 0xFF), (reg_addr & 0xFF)]
        data.extend([x for x in wr_data])
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
        
            
    def i2c_read(self, dev_addr, reg_addr, read_len):
        self.logger.info('Reading I2C device 0x%x, reg 0x%x'%\
                         (dev_addr,reg_addr))
        cmd = self.GET_I2C
        cmd_type = 0x52
        length = 3
        data = [(dev_addr & 0xFF), (reg_addr & 0xFF), (read_len & 0xFF)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def i2c_read_16b(self, dev_addr, reg_addr, read_len):
        self.logger.info('Reading I2C device 0x%x, reg 0x%x'%\
                         (dev_addr,reg_addr))
        cmd = self.GET_I2C_16B
        cmd_type = 0x52
        length = 3
        data = [(dev_addr & 0xFF), (reg_addr & 0xFF), (read_len & 0xFF)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def sensor_i2c_write(self, dev_addr, reg_addr, wr_data):
        self.logger.info('Writing to SENSOR I2C bus, device=0x%x\
                         reg=0x%x'%(dev_addr, reg_addr))
        self.logger.info([hex(i) for i in wr_data])
        cmd = self.SET_SENSOR_I2C
        cmd_type = 0x57
        length = 3+len(wr_data)
        data = [(dev_addr & 0xFF), (reg_addr>>8 & 0xFF), (reg_addr & 0xFF) ]
        data.extend([x for x in wr_data])
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
        
    def sensor_i2c_read(self, dev_addr, reg_addr, read_len):
        self.logger.info('Reading SENSOR I2C device 0x%x, reg 0x%x'%\
                         (dev_addr,reg_addr))
        cmd = self.GET_SENSOR_I2C
        cmd_type = 0x52
        length = 4
        data = [(dev_addr & 0xFF), (reg_addr>>8 & 0xFF), (reg_addr & 0xFF),\
                (read_len & 0xFF)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
        
    def set_spi(self, data):
        self.logger.info('Set SPI data 0x%x'%\
                         (data))
        cmd = self.SET_SPI
        cmd_type = 0x57
        length = 2

        if(self.idd=='new'):
            data = self.split_num(data, split_way=2, endian=0)
        else:
            data = self.split_num(data, split_way=2, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
    
    def set_sensor_param_athena(self, addr, data):
        self.logger.info('Setting Athena Sensor parameter')
        cmd = self.SET_SPI
        cmd_type = 0x57
        length = 4
        data_s = [(addr & 0xFF), (data>>16 & 0xFF), (data>>8 & 0xFF),\
                  (data & 0xFF)]
        packet = self.con_cmd(cmd, cmd_type, length, data_s)
        response = self.send_receive_response(packet)
        return response
    
    def get_sensor_param_athena(self, addr):
        self.logger.info('Getting Athena Sensor parameter')
        cmd = self.GET_SPI
        cmd_type = 0x52
        length = 1
        data =[(addr & 0xFF)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def set_sdram_addr(self, addr):
        self.logger.info('Setting SDRAM address 0x%x'%(addr))
        cmd = self.SET_SDRAM_ADDR
        cmd_type = 0x57
        length = 4
        if(self.idd=='new'):
            data = self.split_num(addr, split_way=4, endian=0)
        else:
            data = self.split_num(addr, split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def set_sdram_data(self, wr_len):
        self.logger.info('Setting SDRAM data (random %d bytes)'%(wr_len))
        cmd = self.SET_SDRAM_DATA
        cmd_type = 0x57
        length = wr_len
        data = [rn.randint(0,255) for x in range(wr_len)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
    
    def set_sdram_data2(self, data):
        self.logger.info('Setting SDRAM data (%d bytes)'%(len(data)))
        cmd = self.SET_SDRAM_DATA
        cmd_type = 0x57
        length = len(data)    
#        data = [rn.randint(0,255) for x in range(wr_len)]
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def get_sdram_data(self, rd_len):
        self.logger.info('Reading SDRAM Data (%d bytes)'%(rd_len))
        cmd = self.GET_SDRAM_DATA
        cmd_type = 0x52
        length = 2
        data = self.split_num(rd_len, split_way=2, endian=0)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def get_qspi_status(self):
        self.logger.info('QSPI status Query')
        cmd = self.QSPI_STATUS_CMD
        cmd_type = 0x52
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 


    def sensor_init_temp_area0_save(self):
        self.logger.info('Sensor Parameters saved in QSPI(low temp. area)')
        cmd = self.TEMP_RANGE0_SENSOR_INIT_WR_QSPI
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 

    def sensor_init_temp_area1_save(self):
        self.logger.info('Sensor Parameters saved in QSPI(high temp. area)')
        cmd = self.TEMP_RANGE1_SENSOR_INIT_WR_QSPI
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 

    def sensor_init_temp_area2_save(self):
        self.logger.info('Sensor Parameters saved in QSPI(high temp. area)')
        cmd = self.TEMP_RANGE2_SENSOR_INIT_WR_QSPI
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 

    def sensor_init_temp_area3_save(self):
        self.logger.info('Sensor Parameters saved in QSPI(high temp. area)')
        cmd = self.TEMP_RANGE3_SENSOR_INIT_WR_QSPI
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 

    def sensor_init_temp_area_save(self, value):
        self.logger.info('Sensor Parameters saved in QSPI( %d area)'%value)
        if(value==0):
            cmd = self.TEMP_RANGE0_SENSOR_INIT_WR_QSPI
        elif(value==1):
            cmd = self.TEMP_RANGE1_SENSOR_INIT_WR_QSPI
        elif(value==2):
            cmd = self.TEMP_RANGE2_SENSOR_INIT_WR_QSPI
        elif(value==3):
            cmd = self.TEMP_RANGE3_SENSOR_INIT_WR_QSPI
        elif(value==4):
            cmd = self.TEMP_RANGE4_SENSOR_INIT_WR_QSPI
        elif(value==5):
            cmd = self.TEMP_RANGE5_SENSOR_INIT_WR_QSPI
        elif(value==6):
            cmd = self.TEMP_RANGE6_SENSOR_INIT_WR_QSPI
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response 
    
    def erase_save_table(self, dest_addr):
        self.logger.info('Erasing and saving in table number %d'%(dest_addr))
        cmd = self.ERASE_SAVE_QSPI 
        length = 4 
        cmd_type = 0x57
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response
    
    def perform_snapshot(self, channel, mode, number_frames):
        self.logger.info('Saving snapshots')
        cmd = self.SNAPSHOT
        length = 4
        cmd_type = 0x57
        dest_addr =  ((channel & 0b111) << 16 | (mode & 0b1111) << 8) | (number_frames & 0xFF)
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def erase_qspi_64KB_new(self, dest_addr,block_num):
        self.logger.info('Erasing %d number of 64KB pool in \
            QSPI address 0x%x'%(dest_addr, block_num))
        cmd = self.ERASE_QSPI 
        cmd_type = 0x57
        length = 8 
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)\
                    +self.split_num(block_num, split_way=4, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)\
                    +self.split_num(block_num, split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def erase_qspi_64KB(self, dest_addr,block_num):
        self.logger.info('Erasing %d number of 64KB pool in \
            QSPI address 0x%x'%(dest_addr, block_num))
        cmd = self.ERASE_QSPI_64KB 
        cmd_type = 0x57
        length = 6
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)\
                    +self.split_num(block_num, split_way=2, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)\
                    +self.split_num(block_num, split_way=2, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def erase_qspi_32KB(self, dest_addr,block_num):
        self.logger.info('Erasing %d number of 32KB pool in \
            QSPI address 0x%x'%(dest_addr, block_num))
        cmd = self.ERASE_QSPI_32KB 
        cmd_type = 0x57
        length = 6 
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)\
                    +self.split_num(block_num, split_way=2, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)\
                    +self.split_num(block_num, split_way=2, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def erase_qspi_4KB(self, dest_addr,block_num):
        self.logger.info('Erasing %d number of 4KB pool in QSPI \
            address 0x%x'%(dest_addr, block_num))
        cmd = self.ERASE_QSPI_4KB 
        cmd_type = 0x57
        length = 6 
        if(self.idd=='new'):
            data = self.split_num(dest_addr,split_way=4, endian=0)\
                    +self.split_num(block_num, split_way=2, endian=0)
        else:
            data = self.split_num(dest_addr,split_way=4, endian=1)\
                    +self.split_num(block_num, split_way=2, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def transfer_data_to_qspi(self, src_addr,dest_addr,transfer_len): 
        self.logger.info('Transfer %d bytes from SDRAM address 0x%x to \
            QSPI address 0x%x'%(transfer_len, src_addr, dest_addr))
        cmd = self.TRANS_SDRAM_TO_QSPI
        cmd_type = 0x57
        length = 12 
        if(self.idd=='new'):
            data = self.split_num(src_addr,split_way=4, endian=0)\
                    +self.split_num(dest_addr, split_way=4, endian=0)\
                    +self.split_num(transfer_len, split_way=4, endian=0)
        else:
            data = self.split_num(src_addr,split_way=4, endian=1)\
                    +self.split_num(dest_addr, split_way=4, endian=1)\
                    +self.split_num(transfer_len, split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def transfer_data_to_sdram(self, src_addr,dest_addr,transfer_len): 
        self.logger.info('Transfer %d bytes from QSPI address 0x%x to \
            SDRAM address 0x%x'%(transfer_len, src_addr, dest_addr))
        cmd = self.TRANS_QSPI_TO_SDRAM
        cmd_type = 0x57
        length = 12 
        if(self.idd=='new'):
            data = self.split_num(src_addr,split_way=4, endian=0)\
                    +self.split_num(dest_addr, split_way=4, endian=0)\
                    +self.split_num(transfer_len, split_way=4, endian=0)
        else:
            data = self.split_num(src_addr,split_way=4, endian=1)\
                    +self.split_num(dest_addr, split_way=4, endian=1)\
                    +self.split_num(transfer_len, split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def transfer_temp_data_to_qspi(self, src_addr,dest_addr,transfer_len): 
        self.logger.info('Transfer %d bytes of temperature data from QSPI \
            address 0x%x to SDRAM address 0x%x'%(transfer_len, src_addr, dest_addr))
        cmd = self.TRANS_TEMP_TO_QSPI
        cmd_type = 0x57
        length = 12 
        if(self.idd=='new'):
            data = self.split_num(src_addr,split_way=4, endian=0)\
                    +self.split_num(dest_addr, split_way=4, endian=0)\
                    +self.split_num(transfer_len, split_way=4, endian=0)
        else:
            data = self.split_num(src_addr,split_way=4, endian=1)\
                    +self.split_num(dest_addr, split_way=4, endian=1)\
                    +self.split_num(transfer_len, split_way=4, endian=1)
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response

    def save_user_settings(self):
        cmd = self.SAVE_USER_SETTINGS
        cmd_type = 0x57
        length = 0
        data = []
        packet = self.con_cmd(cmd, cmd_type, length, data)
        response = self.send_receive_response(packet)
        return response


if __name__ == "__main__":
    ser = serial.Serial('COM9', 115200, timeout=5)
    cmd_gen = CMD(idd='new')
    cmd_gen.set_port(ser)
    cmd_gen.ping(5)
    ser.close()


