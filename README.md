# FramePayloadDecoder
Raw frame payload decoder to json with raw and converted (SI) values

# Briefly about frames sent by PW-Sat2

NOTE: All frames transmitted by the satellite are AX.25 frames. Here, describing "different types of frames" we mean recognition at our application level - frankly speaking we have in mind the content of AX.25 Information Field.

PW-Sat2 transmits lots of frame types that are recognized by us by the first byte of AX.25 Information Field (let's call it "frame payload" for short). Most of the frames are so-called response frames - they confirm that uplink telecommand was received and accepted by the satellite. Another important type is "FileSend" frame that transports chunks of files (containing experiments results and historical telemetry). All those frames are transmitted on demand, never by the satellite itself. However, PW-Sat2 will be sending so-called telemetry frame (beacon) in 60 seconds interval. Each telemetry (beacon) frame has exactly the same fields (i.e. values from the same sensors/subsystems etc.). So it's the most important frame to be parsed.

# Parser

Parsed takes raw frame data - but NOT whole AX.25 frame - Information Field only, so be careful when using it.
If parsed frame is of telemetry (beacon) type - it returns a json object with decoded and converted values. In `example_frames` folder we provide you with some example telemetry frame `telemetry_frame_payload.bin`. But, if provided frame is of different type (check `periodic_frame_payload.bin` and `file_list_frame_payload.bin`) - the returned value is `frame_object` - python object representing frame of particular type.


# How to write telemetry frames parser from scratch, what is the format?

At first, the only valid telemetry frames (beacon) parser is here: https://github.com/PW-Sat2/PWSat2OBC/tree/master/integration_tests/emulator/beacon_parser - the script in this repo (FramePayloadDecoder) also uses this code (as submodule). You can find there valid conversion formulas (from raw to SI units). Be careful, some values are two's complement.


But if you really need to write it on your own, for simplicity, assume such format of payload:

```
| 0xCD | 229 bytes data |
```

1. `0xCD` is telemetry frame marker (beacon). Other frames have different markers here. 
2. 229-bytes data table (be careful and take exact amount of bits, there is no padding to bytes!).

* SI units converters can be found in these files: https://github.com/PW-Sat2/PWSat2OBC/tree/master/integration_tests/emulator/beacon_parser
* If there is no conversion function linked in the table below - the value does not need conversion (or data are solely for diagnostics and needs more investigation than simple conversion formula)
* Note that some values are two's complement (signed type).
* Always cross check results of your own parser with parser from this repository.

|Group Name|Source|Element Name|Size [bit]|Sample rate [s]|Name|Two's complement|Conversion function|
| -------- | ---- | ---------- | -------- | ------------- | -- | -- | -- |
|OBC|Boot loader|Boot Counter|32|once per boot|OBC_Startup_BootCounter| No | |
|||Boot Index|8|once per boot|OBC_Startup_BootIndex| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/startup_parser.py#L5 |
|||OBC Reboot Reason|16|once per boot|OBC_Startup_BootReason| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/startup_parser.py#L23|
|||OBC Code CRC|16|30|OBC_CodeCRC| No | |
||Time Service|Mission Time|64|30|OBC_Time_Mission| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38 |
||Persistent State|External Time|32|30|OBC_Time_External| No | |
||Error Counters|COMM|8|30|OBC_ErrorCounter_COMM| No | |
|||EPS|8|30|OBC_ErrorCounter_EPS| No | |
|||RTC|8|30|OBC_ErrorCounter_RTC| No | |
|||Imtq|8|30|OBC_ErrorCounter_IMTQ| No | |
|||N25q Flash 1|8|30|OBC_ErrorCounter_FLASH_1| No | |
|||N25q Flash 2|8|30|OBC_ErrorCounter_FLASH_2| No | |
|||N25q Flash 3|8|30|OBC_ErrorCounter_FLASH_3| No | |
|||N25q TMR Corrections|8|30|OBC_TMRCounter_FLASH| No | |
|||FRAM TMR Corrections|8|30|OBC_TMRCounter_FRAM| No | |
|||Payload|8|30|OBC_ErrorCounter_PLD| No | |
|||Camera|8|30|OBC_ErrorCounter_CAM| No | |
|||Suns Exp|8|30|OBC_ErrorCounter_SUNS| No | |
|||Antenna primary|8|30|OBC_ErrorCounter_ANTs_Primary| No | |
|||Antenna secondary|8|30|OBC_ErrorCounter_ANTs_Secondary| No | |
||Scrubbing State|Primary Flash Scrubbing pointer|3|30|OBC_Scrubbing_Primary| No | |
|||Secondary Flash Scrubbing pointer|3|30|OBC_Scrubbing_Secondary| No | |
|||RAM Scrubbing pointer|32|30|OBC_Scrubbing_RAM| No | |
||System|Uptime|22|30|OBC_Uptime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38 |
||yaffs|Flash Free Space|32|30|OBC_FLASH_FreeSpace| No | value in bytes |
|Antennas|Antenna Driver|Antenna 1 Deployment Switch Ch A|1|30|ANT_A_1_Switch| No | |
|||Antenna 2 Deployment Switch Ch A|1|30|ANT_A_2_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 3 Deployment Switch Ch A|1|30|ANT_A_3_Switch| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 4 Deployment Switch Ch A|1|30|ANT_A_4_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 1 Deployment Switch Ch B|1|30|ANT_B_1_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 2 Deployment Switch Ch B|1|30|ANT_B_2_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 3 Deployment Switch Ch B|1|30|ANT_B_3_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 4 Deployment Switch Ch B|1|30|ANT_B_4_Switch| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 1 last stop due to time Ch A|1|30|ANT_A_1_LastStopDueToTime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 2 last stop due to time Ch A|1|30|ANT_A_2_LastStopDueToTime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 3 last stop due to time Ch A|1|30|ANT_A_3_LastStopDueToTime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 4 last stop due to time Ch A|1|30|ANT_A_4_LastStopDueToTime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 1 last stop due to time Ch B|1|30|ANT_B_1_LastStopDueToTime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 2 last stop due to time Ch B|1|30|ANT_B_2_LastStopDueToTime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 3 last stop due to time Ch B|1|30|ANT_B_3_LastStopDueToTime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 4 last stop due to time Ch B|1|30|ANT_B_4_LastStopDueToTime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 1 burn active Ch A|1|30|ANT_A_1_BurnActive| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 2 burn active Ch A|1|30|ANT_A_2_BurnActive| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|||Antenna 3 burn active Ch A|1|30|ANT_A_3_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 4 burn active Ch A|1|30|ANT_A_4_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 1 burn active Ch B|1|30|ANT_B_1_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 2 burn active Ch B|1|30|ANT_B_2_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 3 burn active Ch B|1|30|ANT_B_3_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 4 burn active Ch B|1|30|ANT_B_4_BurnActive| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||System independent burn Ch A|1|30|ANT_A_SystemIndependentBurn| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||System independent burn Ch B|1|30|ANT_B_SystemIndependentBurn| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna Ignoring swtiches Ch A|1|30|ANT_A_IgnoringSwitches| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna Ignoring swtiches Ch B|1|30|ANT_B_IgnoringSwitches| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna Armed Ch A|1|30|ANT_A_Armed| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna Armed Ch B|1|30|ANT_B_Armed| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||Antenna 1 Activation Count Ch A|3|30|ANT_A_1_Counter| No | |
|||Antenna 2 Activation Count Ch A|3|30|ANT_A_2_Counter| No | |
|||Antenna 3 Activation Count Ch A|3|30|ANT_A_3_Counter| No | |
|||Antenna 4 Activation Count Ch A|3|30|ANT_A_4_Counter| No | |
|||Antenna 1 Activation Count Ch B|3|30|ANT_B_1_Counter| No | |
|||Antenna 2 Activation Count Ch B|3|30|ANT_B_2_Counter| No | |
|||Antenna 3 Activation Count Ch B|3|30|ANT_B_3_Counter| No | |
|||Antenna 4 Activation Count Ch B|3|30|ANT_B_4_Counter| No | |
|||Antenna 1 Activation Time Ch A|8|30|ANT_A_1_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 2 Activation Time Ch A|8|30|ANT_A_2_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 3 Activation Time Ch A|8|30|ANT_A_3_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 4 Activation Time Ch A|8|30|ANT_A_4_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 1 Activation Time Ch B|8|30|ANT_B_1_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 2 Activation Time Ch B|8|30|ANT_B_2_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 3 Activation Time Ch B|8|30|ANT_B_3_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|||Antenna 4 Activation Time Ch B|8|30|ANT_B_4_Time| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L46|
|Experiments|OBC|Current experiment code|4|30|OBC_Experiments_Code| No |https://github.com/PW-Sat2/PWSat2OBC/blob/1efd37c673907cfeeb85cbe9d01016d33232c2e3/integration_tests/experiment_type.py#L5 |
|||Experiment Starup Result|8|30|OBC_Experiments_StartupResult| No | https://github.com/PW-Sat2/PWSat2OBC/blob/1efd37c673907cfeeb85cbe9d01016d33232c2e3/integration_tests/experiment_type.py#L19|
|||Last Experiment Iteration Status|8|30|OBC_Experiments_LastIterationStatus| No | https://github.com/PW-Sat2/PWSat2OBC/blob/1efd37c673907cfeeb85cbe9d01016d33232c2e3/integration_tests/experiment_type.py#L25|
|Gyroscope|Gyro Driver|X measurement|16|30|GYRO_X| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/gyroscope_telemetry_parser.py#L6|
|||Y measurement|16|30|GYRO_Y| Yes |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/gyroscope_telemetry_parser.py#L6 |
|||Z measurement|16|30|GYRO_Z| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/gyroscope_telemetry_parser.py#L6|
|||Temperature|16|30|GYRO_Temperature| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/gyroscope_telemetry_parser.py#L12|
|COMM|TX|Transmitter Uptime|17|30|COMM_TX_Uptime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38|
|||Bitrate|2|30|COMM_TX_Bitrate| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L58|
|||Last Transmitted RF Reflected Power|12|30|COMM_TX_Power_Reflected_Last| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L44 |
|||Last Transmitted Power Amplifier Temperature|12|30|COMM_TX_Temperature_PowerAmplifier_Last| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L20 |
|||Last Transmitted RF Forward Power|12|30|COMM_TX_Power_Forward_Last| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L44|
|||Last Transmitted Transmitter Current Consumption|12|30|COMM_TX_Current_Last| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L8|
|||Now RF Forward Power|12|30|COMM_TX_Power_Forward_Now| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L44|
|||Now Transmitter Current Consumption|12|30|COMM_TX_Current_Now| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L8|
|||State When Idle|1|30|COMM_TX_IdleState| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
|||BeaconState|1|30|COMM_TX_BeaconState| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
||RX|Uptime|17|30|COMM_RX_Uptime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38|
|||Last Received Doppler Offset|12|30|COMM_RX_Doppler_Last| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L26 |
|||Last Received RSSI|12|30|COMM_RX_RSSI_Last| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L38|
|||Now Doppler Offset|12|30|COMM_RX_Doppler_Now| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L26 |
|||Now Receiver Current Consumption|12|30|COMM_RX_Current| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L14 |
|||Supply Voltage|12|30|COMM_RX_SupplyVoltage| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L32|
|||Oscilator Temperature|12|30|COMM_RX_Temperature_Oscillator| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L20 |
|||Now Power Amplifier Temperature|12|30|COMM_TX_Temperature_PowerAmplifier_Now| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L20 |
|||Now RSSI|12|30|COMM_RX_RSSI_Now| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/comm_telemetry_parser.py#L38|
|Hardware State|GPIO|Sail Deployed|1|30|OBC_SailDeployed| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54|
||MCU|Temperature|12|30|OBC_Temperature| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/mcu_temperature_parser.py#L11 |
|EPS Controller A|Eps Driver|MPPTX.SOL_VOLT|12|30|EPS_A_MPPT_X_SolarVoltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8|
|||MPPTX.SOL_CURR|12|30|EPS_A_MPPT_X_SolarCurrent| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L19|
|||MPPTX.OUT_VOLT|12|30|EPS_A_MPPT_X_OutputVoltage| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8 |
|||MPPTX.TEMP|12|30|EPS_A_MPPT_X_Temperature| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L30|
|||MPPTX.STATE|3|30|EPS_A_MPPT_X_State| No | |
|||MPPTY+.SOL_VOLT|12|30|EPS_A_MPPT_Y+_SolarVoltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8|
|||MPPTY+.SOL_CURR|12|30|EPS_A_MPPT_Y+_SolarCurrent| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L19|
|||MPPTY+.OUT_VOLT|12|30|EPS_A_MPPT_Y+_OutputVoltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8|
|||MPPTY+.TEMP|12|30|EPS_A_MPPT_Y+_Temperature| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L30|
|||MPPTY+.STATE|3|30|EPS_A_MPPT_Y+_State| No | |
|||MPPTY-.SOL_VOLT|12|30|EPS_A_MPPT_Y-_SolarVoltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8|
|||MPPTY-.SOL_CURR|12|30|EPS_A_MPPT_Y-_SolarCurrent| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L19|
|||MPPTY-.OUT_VOLT|12|30|EPS_A_MPPT_Y-_OutputVoltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L8|
|||MPPTY-.TEMP|12|30|EPS_A_MPPT_Y-_Temperature| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L30 |
|||MPPTY-.STATE|3|30|EPS_A_MPPT_Y-_State| No | |
|||DISTR.VOLT_3V3|10|30|EPS_A_Distribution_Voltage_3v3| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L42|
|||DISTR.CURR_3V3|10|30|EPS_A_Distribution_Current_3v3| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L53|
|||DISTR.VOLT_5V|10|30|EPS_A_Distribution_Voltage_5v| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L42|
|||DISTR.CURR_5V|10|30|EPS_A_Distribution_Current_5v| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L53|
|||DISTR.VOLT_VBAT|10|30|EPS_A_Distribution_Voltage_Battery| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L42 |
|||DISTR.CURR_VBAT|10|30|EPS_A_Distribution_Current_Battery| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L53|
|||DISTR.LCL_STATE|7|30|EPS_A_Distribution_LCL_State| No | |
|||DISTR.LCL_FLAGB|6|30|EPS_A_Distribution_LCL_FlagB| No | |
|||BATC.VOLT_A|10|30|EPS_A_BatteryController_Voltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L96 |
|||BATC.CHRG_CURR|10|30|EPS_A_BatteryController_Current_Charge| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L53|
|||BATC.DCHRG_CURR|10|30|EPS_A_BatteryController_Current_Discharge| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L53|
|||BATC.TEMP|10|30|EPS_A_BatteryController_Temperature| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64 |
|||BATC.STATE|3|30|EPS_A_BatteryController_State| No | |
|||BP.TEMP_A|13|30|EPS_A_BatteryPack_Temperature_A| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L78|
|||BP.TEMP_B|13|30|EPS_A_BatteryPack_Temperature_B| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L78|
|||CTRLA.SAFETY-CTR|8|30|EPS_A_SafetyCounter| No | |
|||CTRLA.PWR-CYCLES|16|30|EPS_A_PowerCycleCounter| No | |
|||CTRLA.UPTIME|32|30|EPS_A_Uptime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38|
|||CTRLA.TEMP|10|30|EPS_A_Temperature_MCU| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64 |
|||CTRLA.SUPP_TEMP|10|30|EPS_A_Temperature_Supply| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64|
|||CTRLB.3V3d_VOLT|10|30|EPS_A_Voltage_3v3d| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L85|
|||DCDC.3V3_TEMP|10|30|EPS_A_Temperature_3v3| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64|
|||DCDC.5V_TEMP|10|30|EPS_A_Temperature_5v| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64|
|EPS Controller B|Eps Driver|BP.TEMP_C|10|30|EPS_B_BatteryPack_Temperature| No | |
|||BATC.VOLT_B|10|30|EPS_B_BatteryController_Voltage| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/eps_controller_b_telemetry_parser.py#L8|
|||CTRLB.SAFETY-CTR|8|30|EPS_B_SafetyCounter| No | |
|||CTRLB.PWR-CYCLES|16|30|EPS_B_PowerCycleCounter| No | |
|||CTRLB.UPTIME|32|30|EPS_B_Uptime| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38 |
|||CTRLB.TEMP|10|30|EPS_B_Temperature_MCU| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64 |
|||CTRLB.SUPP_TEMP|10|30|EPS_B_Temperature_Supply| No |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L64 |
|||CTRLA.3V3d_VOLT|10|30|EPS_B_Voltage_3v3d| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/eps_controller_a_telemetry_parser.py#L85|
|Imtq|Imtq Driver|Magnetometer Measurement 1|32|30|IMTQ_Magnetometer_X| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_magnetometers_telemetry_parser.py#L6 |
|||Magnetometer Measurement 2|32|30|IMTQ_Magnetometer_Y| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_magnetometers_telemetry_parser.py#L6|
|||Magnetometer Measurement 3|32|30|IMTQ_Magnetometer_Z| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_magnetometers_telemetry_parser.py#L6|
|Imtq Coil Active|Imtq Driver|Coil active during measurement|1|30|IMTQ_CoilActive| No |https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L54 |
|Imtq Dipole|Imtq Driver|Dipole 1|16|30|IMTQ_Dipole_X| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_dipole_telemetry_parser.py#L6|
|||Dipole 2|16|30|IMTQ_Dipole_Y| Yes |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_dipole_telemetry_parser.py#L6 |
|||Dipole 3|16|30|IMTQ_Dipole_Z| Yes |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_dipole_telemetry_parser.py#L6 |
|Imtq BDot|Imtq Driver|BDot 1|32|30|IMTQ_Bdot_X| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_bdot_telemetry_parser.py#L6|
|||BDot 2|32|30|IMTQ_Bdot_Y| Yes |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_bdot_telemetry_parser.py#L6 |
|||BDot 3|32|30|IMTQ_Bdot_Z| Yes |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_bdot_telemetry_parser.py#L6 |
|Imtq Housekeeping|Imtq Driver|Digital Voltage|16|30|IMTQ_Voltage_Digital| No |https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L6 |
|||Analog Voltage|16|30|IMTQ_Voltage_Analog| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L6|
|||Digital Current|16|30|IMTQ_Current_Digital| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L12|
|||Analog Current|16|30|IMTQ_Current_Analog| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L12|
|||MCU Temperature|16|30|IMTQ_Temperature_MCU| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L18|
|Imtq Coil|Imtq Driver|Coil Current 1|16|30|IMTQ_Current_Coil_X| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L12|
|||Coil Current 2|16|30|IMTQ_Current_Coil_Y| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L12|
|||Coil Current 3|16|30|IMTQ_Current_Coil_Z| No | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L12|
|Imtq Temperature|Imtq Driver|Coil Temperature 1|16|30|IMTQ_Temperature_Coil_X| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L18|
|||Coil Temperature 2|16|30|IMTQ_Temperature_Coil_Y| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L18|
|||Coil Temperature 3|16|30|IMTQ_Temperature_Coil_Z| Yes | https://github.com/PW-Sat2/PWSat2OBC/blob/fc1efd850f20cf595dc274abc4ed9a54667a059d/integration_tests/emulator/beacon_parser/imtq_housekeeping_telemetry_parser.py#L18|
|Imtq state|Imtq Driver|Status|8|30|IMTQ_State_Status| No | |
|||Mode|2|30|IMTQ_State_Mode| No | |
|||Error during previous iteration|8|30|IMTQ_State_ErrorDuringLastIteration| No | |
|||Configuration changed|1|30|IMTQ_State_ConfigurationChanged| No | |
|||Uptime|32|30|IMTQ_State_Uptime| No | https://github.com/PW-Sat2/PWSat2OBC/blob/master/integration_tests/emulator/beacon_parser/units.py#L38|
|Imtq Self Test|Imtq Driver|SelfTest Error INIT|8|once per boot|IMTQ_SelfTest_Error_INIT| No | |
|||SelfTest Error X+|8|once per boot|IMTQ_SelfTest_Error_X+| No | |
|||SelfTest Error X-|8|once per boot|IMTQ_SelfTest_Error_X-| No | |
|||SelfTest Error Y+|8|once per boot|IMTQ_SelfTest_Error_Y+| No | |
|||SelfTest Error Y-|8|once per boot|IMTQ_SelfTest_Error_Y-| No | |
|||SelfTest Error Z+|8|once per boot|IMTQ_SelfTest_Error_Z+| No | |
|||SelfTest Error Z-|8|once per boot|IMTQ_SelfTest_Error_Z-| No | |
|||SelfTest Error FINA|8|once per boot|IMTQ_SelfTest_Error_FINA| No | |

Sum: 1832 bits
