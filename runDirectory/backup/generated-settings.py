### Generated file 43105.4099826389
### IP addresses of master/slave side communication modules
# forward flow: ms_embsys->ms_com->server->ss_com->ss_embsys
# backward flow: ms_embsys<-ms_com<-server<-ss_com<-ss_embsys
 
## testbed computers
"PC_1=""10.114.66.195"""
"PC_2=""NaN"""
"PC_3=""NaN"""
"PC_4=""NaN"""
"PC_5=""NaN"""
 
## testbed modules & testbed computer association
ms_embsys_app_ip=PC_1
ms_com_ip=PC_1
srv_ip=PC_1
ss_com_ip=PC_1
ss_embsys_app_ip=PC_1
 
 
"### enable links (0=> disable, else enable)"
en_kinematic_link=0
en_haptic_link=0
en_audio_link=0
en_video_link=1
 
### set link udp ports
kin_link_0=9000
kin_link_1=9001
kin_link_2=9002
kin_link_3=9003
hap_link_0=9004
hap_link_1=9005
hap_link_2=9006
hap_link_3=9007
audio_link_0=9008
audio_link_1=9009
audio_link_2=9010
audio_link_3=9011
video_link_0=9012
video_link_1=9013
video_link_2=9014
video_link_3=9015
 
###for ms_com (master side communication module)
"ms_com_fwd_flow_kinematic_entry_addr =(ms_com_ip, kin_link_0)"
"ms_com_fwd_flow_kinematic_exit_addr = (srv_ip,kin_link_1) #(ip,port)"
"ms_com_fwd_flow_kinematic_entry_mode =""udp"""
"ms_com_fwd_flow_kinematic_exit_mode = ""udp"""
 
"ms_com_bwd_flow_haptic_entry_addr = (ms_com_ip,hap_link_2) #(ip,port)"
"ms_com_bwd_flow_haptic_exit_addr =('/dev/ttyUSB0',230400)"
"ms_com_bwd_flow_haptic_entry_mode = ""udp"" "
"ms_com_bwd_flow_haptic_exit_mode = ""serial"""
 
"ms_com_bwd_flow_video_entry_addr = (ms_com_ip,video_link_2) "
"ms_com_bwd_flow_video_exit_addr = (ms_embsys_app_ip, video_link_3)"
"ms_com_bwd_flow_video_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"ms_com_bwd_flow_video_exit_mode =""udp"""
 
"ms_com_bwd_flow_audio_entry_addr = (ms_com_ip,audio_link_2) #(ip,port)"
"ms_com_bwd_flow_audio_exit_addr =(ms_embsys_app_ip, audio_link_3)"
"ms_com_bwd_flow_audio_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"ms_com_bwd_flow_audio_exit_mode =""udp"""
 
##for server !!!
"server_fwd_flow_kinematic_entry_addr = (srv_ip,kin_link_1) #(ip,port)"
"server_fwd_flow_kinematic_exit_addr = (ss_com_ip,kin_link_2) #(ip,port)"
"server_fwd_flow_kinematic_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"server_fwd_flow_kinematic_exit_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
 
"server_bwd_flow_haptic_entry_addr = (srv_ip,hap_link_1) #(ip,port)"
"server_bwd_flow_haptic_exit_addr = (ms_com_ip,hap_link_2) #(ip,port)"
"server_bwd_flow_haptic_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"server_bwd_flow_haptic_exit_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
 
"server_bwd_flow_video_entry_addr = (srv_ip,video_link_1) #(ip,port)"
"server_bwd_flow_video_exit_addr = (ms_com_ip,video_link_2) #(ip,port)"
"server_bwd_flow_video_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"server_bwd_flow_video_exit_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
 
"server_bwd_flow_audio_entry_addr = (srv_ip,audio_link_1) #(ip,port)"
"server_bwd_flow_audio_exit_addr = (ms_com_ip,audio_link_2) #(ip,port)"
"server_bwd_flow_audio_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"server_bwd_flow_audio_exit_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
 
##for ss_com (slave side communication module)
"ss_com_fwd_flow_kinematic_entry_addr = (ss_com_ip,kin_link_2) #(ip,port)"
"ss_com_fwd_flow_kinematic_exit_addr = ('/dev/ttyUSB0',115200)"
"ss_com_fwd_flow_kinematic_entry_mode = ""udp"" #""udp""/""file""/""serial""/""local"""
"ss_com_fwd_flow_kinematic_exit_mode = ""serial"""
 
"ss_com_bwd_flow_haptic_entry_addr = ('/dev/ttyUSB0',115200) #(ip,port)"
"ss_com_bwd_flow_haptic_exit_addr = ('/dev/ttyUSB0',115200)"
"ss_com_bwd_flow_haptic_entry_mode = ""serial"""
"ss_com_bwd_flow_haptic_exit_mode = ""serial"""
 
"ss_com_bwd_flow_video_entry_addr = (ss_com_ip, video_link_0)"
"ss_com_bwd_flow_video_exit_addr = (srv_ip,video_link_1) #(ip,port)"
"ss_com_bwd_flow_video_entry_mode =""udp"""
"ss_com_bwd_flow_video_exit_mode = ""udp"" "
 
"ss_com_bwd_flow_audio_entry_addr = (ss_com_ip, audio_link_0)"
"ss_com_bwd_flow_audio_exit_addr = (srv_ip,audio_link_1) #(ip,port)"
"ss_com_bwd_flow_audio_entry_mode = ""udp"""
"ss_com_bwd_flow_audio_exit_mode = ""udp"" "
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
