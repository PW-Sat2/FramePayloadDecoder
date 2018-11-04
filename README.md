# FramePayloadDecoder
Raw frame payload decoder to json with raw and converted (SI) values

# Briefly about frames sent by PW-Sat2

NOTE: All frames transmitted by the satellite are AX.25 frames. Here, describing "different types of frames" I mean recognition at our application level - frankly speaking I have in mind the content of AX.25 Information Field.

So, PW-Sat2 will transmitt lots of frame types that are recognized by us by the first byte of AX.25 Information Field (let's call it "frame payload" for short). Most of the frames are so-called response frames - they confirm that uplink telecommand was received and accepted by the satellite. Another important type is "FileSend" frame that transports chunks of experiment's files. All those frames are transmitted on demand, never by the satellite itself. However, PW-Sat2 will be sending so-called telemetry frame (beacon) in 60 seconds interval. Each telemetry (beacon) frame has exactly the same fields (i.e. values from the same sensors/subsystems etc.). So it's the most important frame to be parsed.

# Parser

Parsed takes raw frame data - but NOT whole AX.25 frame - Information Field only, so be careful when using it.
If parsed frame is of telemetry (beacon) type - it returns a json object with decoded and converted values. In `example_frames` folder I provide you with some example telemetry frame `telemetry_frame_payload.bin`. But, if provided frame is of different type (check `periodic_frame_payload.bin` and `file_list_frame_payload.bin`) - the returned value is `frame_object` - python object representing frame of particular type.

# What would be beneficial for PW-Sat2 and others (SatNOGS)?

Minimal plan is to get `.ogg` files (as in PicSat case - take look at it's recording @ SatNOGS) so we can decode content by our own.

If possible, we would like to get decoded `.frames` files - the format is described here: https://github.com/PW-Sat2/HAMRadio/wiki/Received-frames-list-and-%22.frames%22-files#format-of-frames-file. "Downlink.grc" GNURadio flow graphs has our out-of-tree block to save such files. It's just base64 encoded frames with timestamp (in csv) so we can upload it to radio.pw-sat.pl and show results not only to HAM radio but wide publicity (in plots for instance). So it would be really great to have such functionallity on SatNOGS.

Another possibility is that SatNOGS will decode telemetry (beacon) frames to json format as in this parser/decoder.


# I would like to write telemetry frames parser from scratch, what is the format?

At first, the only valid telemetry frames (beacon) parser is here: https://github.com/PW-Sat2/PWSat2OBC/tree/master/integration_tests/emulator/beacon_parser - the script in this repo (FramePayloadDecoder) also uses this code (as submodule). You can find there valid conversion formulas (from raw to SI units). Be careful, some values are two's complement.


But if you really need to write it on your own, for simplicity, assume such format of payload:

```
| 0xCD | 229 bytes data |
```

`0xCD` is telemetry frame marker. Other frames have different markers here.

229-bytes data table (be careful and take exact amount of bits, there is no padding to bytes to save data amount):


|Group Name|Source|Element Name|Size [bit]|Sample rate [s]|To plot|Conversion formula|Name|
|OBC|Boot loader|Boot Counter|32|once per boot|||OBC_Startup_BootCounter|
|||Boot Index|8|once per boot|||OBC_Startup_BootIndex|
|||OBC Reboot Reason|16|once per boot|||OBC_Startup_BootReason|
|||OBC Code CRC|16|30|||OBC_CodeCRC|
||Time Service|Mission Time|64|30|||OBC_Time_Mission|
||Persistent State|External Time|32|30|||OBC_Time_External|
||Error Counters|COMM|8|30|||OBC_ErrorCounter_COMM|
|||EPS|8|30|||OBC_ErrorCounter_EPS|
|||RTC|8|30|||OBC_ErrorCounter_RTC|
|||Imtq|8|30|||OBC_ErrorCounter_IMTQ|
|||N25q Flash 1|8|30|||OBC_ErrorCounter_FLASH_1|
|||N25q Flash 2|8|30|||OBC_ErrorCounter_FLASH_2|
|||N25q Flash 3|8|30|||OBC_ErrorCounter_FLASH_3|
|||N25q TMR Corrections|8|30|||OBC_TMRCounter_FLASH|
|||FRAM TMR Corrections|8|30|||OBC_TMRCounter_FRAM|
|||Payload|8|30|||OBC_ErrorCounter_PLD|
|||Camera|8|30|||OBC_ErrorCounter_CAM|
|||Suns Exp|8|30|||OBC_ErrorCounter_SUNS|
|||Antenna primary|8|30|||OBC_ErrorCounter_ANTs_Primary|
|||Antenna secondary|8|30|||OBC_ErrorCounter_ANTs_Secondary|
||Scrubbing State|Primary Flash Scrubbing pointer|3|30|||OBC_Scrubbing_Primary|
|||Secondary Flash Scrubbing pointer|3|30|||OBC_Scrubbing_Secondary|
|||RAM Scrubbing pointer|32|30|||OBC_Scrubbing_RAM|
||System|Uptime|22|30|||OBC_Uptime|
||yaffs|Flash Free Space|32|30|||OBC_FLASH_FreeSpace|
|Antennas|Antenna Driver|Antenna 1 Deployment Switch Ch A|1|30|||ANT_A_1_Switch|
|||Antenna 2 Deployment Switch Ch A|1|30|||ANT_A_2_Switch|
|||Antenna 3 Deployment Switch Ch A|1|30|||ANT_A_3_Switch|
|||Antenna 4 Deployment Switch Ch A|1|30|||ANT_A_4_Switch|
|||Antenna 1 Deployment Switch Ch B|1|30|||ANT_B_1_Switch|
|||Antenna 2 Deployment Switch Ch B|1|30|||ANT_B_2_Switch|
|||Antenna 3 Deployment Switch Ch B|1|30|||ANT_B_3_Switch|
|||Antenna 4 Deployment Switch Ch B|1|30|||ANT_B_4_Switch|
|||Antenna 1 last stop due to time Ch A|1|30|||ANT_A_1_LastStopDueToTime|
|||Antenna 2 last stop due to time Ch A|1|30|||ANT_A_2_LastStopDueToTime|
|||Antenna 3 last stop due to time Ch A|1|30|||ANT_A_3_LastStopDueToTime|
|||Antenna 4 last stop due to time Ch A|1|30|||ANT_A_4_LastStopDueToTime|
|||Antenna 1 last stop due to time Ch B|1|30|||ANT_B_1_LastStopDueToTime|
|||Antenna 2 last stop due to time Ch B|1|30|||ANT_B_2_LastStopDueToTime|
|||Antenna 3 last stop due to time Ch B|1|30|||ANT_B_3_LastStopDueToTime|
|||Antenna 4 last stop due to time Ch B|1|30|||ANT_B_4_LastStopDueToTime|
|||Antenna 1 burn active Ch A|1|30|||ANT_A_1_BurnActive|
|||Antenna 2 burn active Ch A|1|30|||ANT_A_2_BurnActive|
|||Antenna 3 burn active Ch A|1|30|||ANT_A_3_BurnActive|
|||Antenna 4 burn active Ch A|1|30|||ANT_A_4_BurnActive|
|||Antenna 1 burn active Ch B|1|30|||ANT_B_1_BurnActive|
|||Antenna 2 burn active Ch B|1|30|||ANT_B_2_BurnActive|
|||Antenna 3 burn active Ch B|1|30|||ANT_B_3_BurnActive|
|||Antenna 4 burn active Ch B|1|30|||ANT_B_4_BurnActive|
|||System independent burn Ch A|1|30|||ANT_A_SystemIndependentBurn|
|||System independent burn Ch B|1|30|||ANT_B_SystemIndependentBurn|
|||Antenna Ignoring swtiches Ch A|1|30|||ANT_A_IgnoringSwitches|
|||Antenna Ignoring swtiches Ch B|1|30|||ANT_B_IgnoringSwitches|
|||Antenna Armed Ch A|1|30|||ANT_A_Armed|
|||Antenna Armed Ch B|1|30|||ANT_B_Armed|
|||Antenna 1 Activation Count Ch A|3|30|||ANT_A_1_Counter|
|||Antenna 2 Activation Count Ch A|3|30|||ANT_A_2_Counter|
|||Antenna 3 Activation Count Ch A|3|30|||ANT_A_3_Counter|
|||Antenna 4 Activation Count Ch A|3|30|||ANT_A_4_Counter|
|||Antenna 1 Activation Count Ch B|3|30|||ANT_B_1_Counter|
|||Antenna 2 Activation Count Ch B|3|30|||ANT_B_2_Counter|
|||Antenna 3 Activation Count Ch B|3|30|||ANT_B_3_Counter|
|||Antenna 4 Activation Count Ch B|3|30|||ANT_B_4_Counter|
|||Antenna 1 Activation Time Ch A|8|30||1 LSB == 2 seconds|ANT_A_1_Time|
|||Antenna 2 Activation Time Ch A|8|30||1 LSB == 2 seconds|ANT_A_2_Time|
|||Antenna 3 Activation Time Ch A|8|30||1 LSB == 2 seconds|ANT_A_3_Time|
|||Antenna 4 Activation Time Ch A|8|30||1 LSB == 2 seconds|ANT_A_4_Time|
|||Antenna 1 Activation Time Ch B|8|30||1 LSB == 2 seconds|ANT_B_1_Time|
|||Antenna 2 Activation Time Ch B|8|30||1 LSB == 2 seconds|ANT_B_2_Time|
|||Antenna 3 Activation Time Ch B|8|30||1 LSB == 2 seconds|ANT_B_3_Time|
|||Antenna 4 Activation Time Ch B|8|30||1 LSB == 2 seconds|ANT_B_4_Time|
|Experiments|OBC|Current experiment code|4|30|||OBC_Experiments_Code|
|||Experiment Starup Result|8|30|||OBC_Experiments_StartupResult|
|||Last Experiment Iteration Status|8|30|||OBC_Experiments_LastIterationStatus|
|Gyroscope|Gyro Driver|X measurement|16|30|x|`rate = raw/14.375 [deg/s]`|GYRO_X|
|||Y measurement|16|30|x|`rate = raw/14.375 [deg/s]`|GYRO_Y|
|||Z measurement|16|30|x|`rate = raw/14.375 [deg/s]`|GYRO_Z|
|||Temperature|16|30|x|`temperature = (raw + 23000)/280 [degC]`|GYRO_Temperature|
|COMM|TX|Transmitter Uptime|17|30||1 LSB == 1 second|COMM_TX_Uptime|
|||Bitrate|2|30||0 - 1200; 1-2400; 2-4800; 3-9600bps|COMM_TX_Bitrate|
|||Last Transmitted RF Reflected Power|12|30|x||COMM_TX_Power_Reflected_Last|
|||Last Transmitted Power Amplifier Temperature|12|30|x||COMM_TX_Temperature_PowerAmplifier_Last|
|||Last Transmitted RF Forward Power|12|30|x||COMM_TX_Power_Forward_Last|
|||Last Transmitted Transmitter Current Consumption|12|30|x||COMM_TX_Current_Last|
|||Now RF Forward Power|12|30|x||COMM_TX_Power_Forward_Now|
|||Now Transmitter Current Consumption|12|30|x||COMM_TX_Current_Now|
|||State When Idle|1|30|x||COMM_TX_IdleState|
|||BeaconState|1|30|x||COMM_TX_BeaconState|
||RX|Uptime|17|30|x|1 LSB == 1 second|COMM_RX_Uptime|
|||Last Received Doppler Offset|12|30|||COMM_RX_Doppler_Last|
|||Last Received RSSI|12|30|||COMM_RX_RSSI_Last|
|||Now Doppler Offset|12|30|||COMM_RX_Doppler_Now|
|||Now Receiver Current Consumption|12|30|||COMM_RX_Current|
|||Supply Voltage|12|30|||COMM_RX_SupplyVoltage|
|||Oscilator Temperature|12|30|||COMM_RX_Temperature_Oscillator|
|||Now Power Amplifier Temperature|12|30|||COMM_TX_Temperature_PowerAmplifier_Now|
|||Now RSSI|12|30|||COMM_RX_RSSI_Now|
|Hardware State|GPIO|Sail Deployed|1|30|||OBC_SailDeployed|
||MCU|Temperature|12|30|x||OBC_Temperature|
|EPS Controller A|Eps Driver|MPPTX.SOL_VOLT|12|30|x||EPS_A_MPPT_X_SolarVoltage|
|||MPPTX.SOL_CURR|12|30|x||EPS_A_MPPT_X_SolarCurrent|
|||MPPTX.OUT_VOLT|12|30|x||EPS_A_MPPT_X_OutputVoltage|
|||MPPTX.TEMP|12|30|x||EPS_A_MPPT_X_Temperature|
|||MPPTX.STATE|3|30|||EPS_A_MPPT_X_State|
|||MPPTY+.SOL_VOLT|12|30|x||EPS_A_MPPT_Y+_SolarVoltage|
|||MPPTY+.SOL_CURR|12|30|x||EPS_A_MPPT_Y+_SolarCurrent|
|||MPPTY+.OUT_VOLT|12|30|x||EPS_A_MPPT_Y+_OutputVoltage|
|||MPPTY+.TEMP|12|30|x||EPS_A_MPPT_Y+_Temperature|
|||MPPTY+.STATE|3|30|||EPS_A_MPPT_Y+_State|
|||MPPTY-.SOL_VOLT|12|30|x||EPS_A_MPPT_Y-_SolarVoltage|
|||MPPTY-.SOL_CURR|12|30|x||EPS_A_MPPT_Y-_SolarCurrent|
|||MPPTY-.OUT_VOLT|12|30|x||EPS_A_MPPT_Y-_OutputVoltage|
|||MPPTY-.TEMP|12|30|x||EPS_A_MPPT_Y-_Temperature|
|||MPPTY-.STATE|3|30|||EPS_A_MPPT_Y-_State|
|||DISTR.VOLT_3V3|10|30|x||EPS_A_Distribution_Voltage_3v3|
|||DISTR.CURR_3V3|10|30|x||EPS_A_Distribution_Current_3v3|
|||DISTR.VOLT_5V|10|30|x||EPS_A_Distribution_Voltage_5v|
|||DISTR.CURR_5V|10|30|x||EPS_A_Distribution_Current_5v|
|||DISTR.VOLT_VBAT|10|30|x||EPS_A_Distribution_Voltage_Battery|
|||DISTR.CURR_VBAT|10|30|x||EPS_A_Distribution_Current_Battery|
|||DISTR.LCL_STATE|7|30|||EPS_A_Distribution_LCL_State|
|||DISTR.LCL_FLAGB|6|30||6 bits; error - '0'|EPS_A_Distribution_LCL_FlagB|
|||BATC.VOLT_A|10|30|x||EPS_A_BatteryController_Voltage|
|||BATC.CHRG_CURR|10|30|x||EPS_A_BatteryController_Current_Charge|
|||BATC.DCHRG_CURR|10|30|x||EPS_A_BatteryController_Current_Discharge|
|||BATC.TEMP|10|30|x||EPS_A_BatteryController_Temperature|
|||BATC.STATE|3|30|||EPS_A_BatteryController_State|
|||BP.TEMP_A|13|30|x||EPS_A_BatteryPack_Temperature_A|
|||BP.TEMP_B|13|30|x||EPS_A_BatteryPack_Temperature_B|
|||CTRLA.SAFETY-CTR|8|30|||EPS_A_SafetyCounter|
|||CTRLA.PWR-CYCLES|16|30|x||EPS_A_PowerCycleCounter|
|||CTRLA.UPTIME|32|30|x||EPS_A_Uptime|
|||CTRLA.TEMP|10|30|x||EPS_A_Temperature_MCU|
|||CTRLA.SUPP_TEMP|10|30|x||EPS_A_Temperature_Supply|
|||CTRLB.3V3d_VOLT|10|30|x||EPS_A_Voltage_3v3d|
|||DCDC.3V3_TEMP|10|30|x||EPS_A_Temperature_3v3|
|||DCDC.5V_TEMP|10|30|x||EPS_A_Temperature_5v|
|EPS Controller B|Eps Driver|BP.TEMP_C|10|30|x||EPS_B_BatteryPack_Temperature|
|||BATC.VOLT_B|10|30|x||EPS_B_BatteryController_Voltage|
|||CTRLB.SAFETY-CTR|8|30|||EPS_B_SafetyCounter|
|||CTRLB.PWR-CYCLES|16|30|x||EPS_B_PowerCycleCounter|
|||CTRLB.UPTIME|32|30|x||EPS_B_Uptime|
|||CTRLB.TEMP|10|30|x||EPS_B_Temperature_MCU|
|||CTRLB.SUPP_TEMP|10|30|x||EPS_B_Temperature_Supply|
|||CTRLA.3V3d_VOLT|10|30|x||EPS_B_Voltage_3v3d|
|Imtq|Imtq Driver|Magnetometer Measurement 1|32|30|x||IMTQ_Magnetometer_X|
|||Magnetometer Measurement 2|32|30|x||IMTQ_Magnetometer_Y|
|||Magnetometer Measurement 3|32|30|x||IMTQ_Magnetometer_Z|
|Imtq Coil Active|Imtq Driver|Coil active during measurement|1|30|||IMTQ_CoilActive|
|Imtq Dipole|Imtq Driver|Dipole 1|16|30|x||IMTQ_Dipole_X|
|||Dipole 2|16|30|x||IMTQ_Dipole_Y|
|||Dipole 3|16|30|x||IMTQ_Dipole_Z|
|Imtq BDot|Imtq Driver|BDot 1|32|30|x||IMTQ_Bdot_X|
|||BDot 2|32|30|x||IMTQ_Bdot_Y|
|||BDot 3|32|30|x||IMTQ_Bdot_Z|
|Imtq Housekeeping|Imtq Driver|Digital Voltage|16|30|x||IMTQ_Voltage_Digital|
|||Analog Voltage|16|30|x||IMTQ_Voltage_Analog|
|||Digital Current|16|30|x||IMTQ_Current_Digital|
|||Analog Current|16|30|x||IMTQ_Current_Analog|
|||MCU Temperature|16|30|x||IMTQ_Temperature_MCU|
|Imtq Coil|Imtq Driver|Coil Current 1|16|30|x||IMTQ_Current_Coil_X|
|||Coil Current 2|16|30|x||IMTQ_Current_Coil_Y|
|||Coil Current 3|16|30|x||IMTQ_Current_Coil_Z|
|Imtq Temperature|Imtq Driver|Coil Temperature 1|16|30|x||IMTQ_Temperature_Coil_X|
|||Coil Temperature 2|16|30|x||IMTQ_Temperature_Coil_Y|
|||Coil Temperature 3|16|30|x||IMTQ_Temperature_Coil_Z|
|Imtq state|Imtq Driver|Status|8|30|||IMTQ_State_Status|
|||Mode|2|30|||IMTQ_State_Mode|
|||Error during previous iteration|8|30|||IMTQ_State_ErrorDuringLastIteration|
|||Configuration changed|1|30|||IMTQ_State_ConfigurationChanged|
|||Uptime|32|30|x||IMTQ_State_Uptime|
|Imtq Self Test|Imtq Driver|SelfTest Error INIT|8|once per boot|||IMTQ_SelfTest_Error_INIT|
|||SelfTest Error X+|8|once per boot|||IMTQ_SelfTest_Error_X+|
|||SelfTest Error X-|8|once per boot|||IMTQ_SelfTest_Error_X-|
|||SelfTest Error Y+|8|once per boot|||IMTQ_SelfTest_Error_Y+|
|||SelfTest Error Y-|8|once per boot|||IMTQ_SelfTest_Error_Y-|
|||SelfTest Error Z+|8|once per boot|||IMTQ_SelfTest_Error_Z+|
|||SelfTest Error Z-|8|once per boot|||IMTQ_SelfTest_Error_Z-|
|||SelfTest Error FINA|8|once per boot|||IMTQ_SelfTest_Error_FINA|

Sum: 1832 bits