Search.setIndex({docnames:["aed_load","api","autoapi/emu/auth/index","autoapi/emu/backend/index","autoapi/emu/cli/index","autoapi/emu/download/index","autoapi/emu/index","autoapi/emu/luigi/box/index","autoapi/emu/luigi/index","autoapi/emu/meds/index","autoapi/emu/names/index","autoapi/emu/neuralynx_io/index","autoapi/emu/nwb/index","autoapi/emu/pdil/index","autoapi/emu/pdil/raw/index","autoapi/emu/pipeline/download/index","autoapi/emu/pipeline/index","autoapi/emu/pipeline/process/index","autoapi/emu/pipeline/remote/index","autoapi/emu/pipeline/timestamps/index","autoapi/emu/pipeline/utils/index","autoapi/emu/process_videos/index","autoapi/emu/utils/index","box_integration","intro","markdown","notebooks","pt6305-day2-preprocessing"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,"sphinxcontrib.bibtex":7,sphinx:56},filenames:["aed_load.ipynb","api.rst","autoapi/emu/auth/index.rst","autoapi/emu/backend/index.rst","autoapi/emu/cli/index.rst","autoapi/emu/download/index.rst","autoapi/emu/index.rst","autoapi/emu/luigi/box/index.rst","autoapi/emu/luigi/index.rst","autoapi/emu/meds/index.rst","autoapi/emu/names/index.rst","autoapi/emu/neuralynx_io/index.rst","autoapi/emu/nwb/index.rst","autoapi/emu/pdil/index.rst","autoapi/emu/pdil/raw/index.rst","autoapi/emu/pipeline/download/index.rst","autoapi/emu/pipeline/index.rst","autoapi/emu/pipeline/process/index.rst","autoapi/emu/pipeline/remote/index.rst","autoapi/emu/pipeline/timestamps/index.rst","autoapi/emu/pipeline/utils/index.rst","autoapi/emu/process_videos/index.rst","autoapi/emu/utils/index.rst","box_integration.md","intro.md","markdown.md","notebooks.ipynb","pt6305-day2-preprocessing.ipynb"],objects:{"":[[6,0,0,"-","emu"]],"emu.auth":[[2,1,1,"","DEFAULT_CONFIG"],[2,1,1,"","DEFAULT_ROOT"],[2,1,1,"","auth"],[2,2,1,"","jwt"]],"emu.backend":[[3,2,1,"","add_collaborator"],[3,1,1,"","folder_app"],[3,2,1,"","get_file_manifest"],[3,2,1,"","list"]],"emu.cli":[[4,2,1,"","download"],[4,2,1,"","info"],[4,2,1,"","main"],[4,2,1,"","preprocess"]],"emu.download":[[5,2,1,"","dl_file"]],"emu.luigi":[[7,0,0,"-","box"]],"emu.luigi.box":[[7,3,1,"","AtomicWritableBoxFile"],[7,3,1,"","BoxClient"],[7,3,1,"","BoxTarget"],[7,1,1,"","DEFAULT_CONFIG_FP"],[7,3,1,"","ReadableBoxFile"],[7,2,1,"","accept_trailing_slash"],[7,2,1,"","accept_trailing_slash_in_existing_dirpaths"],[7,2,1,"","file_id_to_path"],[7,2,1,"","folder_id_to_path"],[7,1,1,"","logger"],[7,2,1,"","obj_to_path"],[7,2,1,"","path_to_fid"],[7,2,1,"","path_to_obj"],[7,2,1,"","path_to_root"]],"emu.luigi.box.AtomicWritableBoxFile":[[7,4,1,"","move_to_final_destination"]],"emu.luigi.box.BoxClient":[[7,4,1,"","_exists_and_is_dir"],[7,4,1,"","download_as_bytes"],[7,4,1,"","exists"],[7,4,1,"","file"],[7,4,1,"","file_id_to_path"],[7,4,1,"","folder"],[7,4,1,"","isdir"],[7,4,1,"","mkdir"],[7,4,1,"","path_to_fid"],[7,4,1,"","remove"],[7,4,1,"","upload"]],"emu.luigi.box.BoxTarget":[[7,4,1,"","fs"],[7,4,1,"","open"],[7,4,1,"","temporary_file"],[7,4,1,"","temporary_path"]],"emu.luigi.box.ReadableBoxFile":[[7,4,1,"","__del__"],[7,4,1,"","__enter__"],[7,4,1,"","__exit__"],[7,4,1,"","close"],[7,4,1,"","download_to_tmp"],[7,4,1,"","read"],[7,4,1,"","readable"],[7,4,1,"","seekable"],[7,4,1,"","writable"]],"emu.meds":[[9,3,1,"","Drug"],[9,3,1,"","DrugAdministration"],[9,3,1,"","Lacosamide"],[9,3,1,"","Lamotrigine"],[9,3,1,"","Levetiracetam"],[9,3,1,"","Pregabalin"],[9,2,1,"","gen_norm_dist"]],"emu.meds.Drug":[[9,4,1,"","__str__"],[9,5,1,"","_weight"],[9,4,1,"","get_CL"],[9,4,1,"","show_CL"],[9,4,1,"","show_Vd"]],"emu.meds.DrugAdministration":[[9,4,1,"","C"],[9,4,1,"","CL"],[9,4,1,"","Css"],[9,4,1,"","Tmax"],[9,4,1,"","Vd"],[9,4,1,"","plot"],[9,4,1,"","plot_Cp"],[9,4,1,"","set_baseline"],[9,4,1,"","u"]],"emu.meds.Lacosamide":[[9,5,1,"","CL_dist"],[9,5,1,"","F"],[9,5,1,"","Tmax_dist"],[9,5,1,"","_CL"],[9,5,1,"","_Tmax"],[9,5,1,"","_Vd"],[9,5,1,"","_name_"],[9,4,1,"","create_administration"]],"emu.meds.Lamotrigine":[[9,5,1,"","CL_dist"],[9,5,1,"","F"],[9,5,1,"","Tmax_dist"],[9,5,1,"","Vd_dist"],[9,5,1,"","_CL"],[9,5,1,"","_Tmax"],[9,5,1,"","_Vd"],[9,5,1,"","_name_"],[9,4,1,"","create_administration"]],"emu.meds.Levetiracetam":[[9,5,1,"","F"],[9,5,1,"","_CL"],[9,5,1,"","_Tmax"],[9,5,1,"","_Vd"],[9,5,1,"","_name_"],[9,4,1,"","create_administration"]],"emu.meds.Pregabalin":[[9,5,1,"","CL_dist"],[9,5,1,"","F"],[9,5,1,"","_CL"],[9,5,1,"","_Tmax"],[9,5,1,"","_Vd"],[9,5,1,"","_name_"],[9,4,1,"","create_administration"],[9,4,1,"","get_CL"],[9,4,1,"","show_CL"]],"emu.names":[[10,1,1,"","FEDERATION_STARSHIPS"],[10,2,1,"","federation_starships"]],"emu.neuralynx_io":[[11,1,1,"","HEADER_LENGTH"],[11,1,1,"","MICROVOLT_SCALING"],[11,1,1,"","MILLIVOLT_SCALING"],[11,1,1,"","NCS_RECORD"],[11,1,1,"","NCS_SAMPLES_PER_RECORD"],[11,1,1,"","NEV_RECORD"],[11,1,1,"","VOLT_SCALING"],[11,2,1,"","check_ncs_records"],[11,2,1,"","estimate_record_count"],[11,2,1,"","load_ncs"],[11,2,1,"","load_nev"],[11,2,1,"","nev_as_records"],[11,2,1,"","parse_header"],[11,2,1,"","parse_neuralynx_time_string"],[11,2,1,"","read_header"],[11,2,1,"","read_records"]],"emu.nwb":[[12,2,1,"","add_electrodes"],[12,2,1,"","add_ttl"],[12,2,1,"","get_channel_id"],[12,2,1,"","initialize_nwb"],[12,2,1,"","iter_ncs_to_timeseries"],[12,2,1,"","label_blockstart"],[12,2,1,"","ncs_to_grp_eseries"],[12,2,1,"","ncs_to_nwb"],[12,2,1,"","ncs_to_nwb_raw"],[12,2,1,"","ncs_to_timeseries"],[12,2,1,"","nev_to_behavior_annotation"],[12,2,1,"","nlx_to_nwb"]],"emu.pdil":[[14,0,0,"-","raw"]],"emu.pdil.raw":[[14,3,1,"","Electrophysiology"],[14,1,1,"","PAYOFF_DICT"],[14,3,1,"","Participant"],[14,2,1,"","extract_trial_timing"],[14,2,1,"","get_data_manifest"],[14,2,1,"","points_to_choice"],[14,2,1,"","taskoutput_meta"],[14,2,1,"","timestamps"]],"emu.pdil.raw.Electrophysiology":[[14,4,1,"","events"],[14,4,1,"","gen_nlx_chunks"],[14,4,1,"","load_all_nev"],[14,4,1,"","to_nwb"],[14,4,1,"","ttl"]],"emu.pdil.raw.Participant":[[14,4,1,"","add_behavior"],[14,4,1,"","cache_behavior"],[14,4,1,"","cache_ncs"],[14,4,1,"","cache_nev"],[14,4,1,"","create_nwb"],[14,4,1,"","load_game_data"],[14,4,1,"","load_pdil_events"]],"emu.pipeline":[[15,0,0,"-","download"],[17,0,0,"-","process"],[18,0,0,"-","remote"],[19,0,0,"-","timestamps"],[20,0,0,"-","utils"]],"emu.pipeline.download":[[15,3,1,"","BehaviorRaw"],[15,3,1,"","CacheData"],[15,3,1,"","CacheTaskOutput"],[15,3,1,"","CollectionBuilder"],[15,3,1,"","ExperimentManifest"],[15,3,1,"","FileManifest"],[15,3,1,"","NLXRaw"],[15,3,1,"","PatientsLocal"],[15,3,1,"","Raw"],[15,2,1,"","cache_fp"],[15,2,1,"","check_or_create"],[15,2,1,"","sha1"]],"emu.pipeline.download.BehaviorRaw":[[15,5,1,"","__name__"],[15,4,1,"","cache_fp"],[15,4,1,"","out_dir"],[15,5,1,"","patient_id"],[15,5,1,"","study"]],"emu.pipeline.download.CacheData":[[15,5,1,"","data_root"],[15,5,1,"","patient_id"],[15,4,1,"","requires"]],"emu.pipeline.download.CacheTaskOutput":[[15,4,1,"","output"],[15,4,1,"","run"]],"emu.pipeline.download.CollectionBuilder":[[15,4,1,"","_create_seeg_path"],[15,4,1,"","clean"],[15,4,1,"","from_dataframe"],[15,4,1,"","gen_ncs"],[15,4,1,"","nev"]],"emu.pipeline.download.ExperimentManifest":[[15,4,1,"","create"],[15,5,1,"","data_root"],[15,5,1,"","file_name"],[15,4,1,"","load"],[15,4,1,"","out_dir"],[15,4,1,"","output"],[15,4,1,"","requires"],[15,4,1,"","run"],[15,5,1,"","study"]],"emu.pipeline.download.FileManifest":[[15,5,1,"","data_root"],[15,4,1,"","output"],[15,5,1,"","patient_id"],[15,4,1,"","requires"],[15,4,1,"","run"]],"emu.pipeline.download.NLXRaw":[[15,5,1,"","__name__"],[15,4,1,"","cache_fp"],[15,4,1,"","out_dir"],[15,5,1,"","patient_id"],[15,5,1,"","study"]],"emu.pipeline.download.PatientsLocal":[[15,5,1,"","data_root"],[15,5,1,"","file_id"],[15,4,1,"","output"],[15,4,1,"","run"]],"emu.pipeline.download.Raw":[[15,5,1,"","__name__"],[15,4,1,"","__repr__"],[15,5,1,"","data_root"],[15,4,1,"","download"],[15,5,1,"","file_id"],[15,5,1,"","file_name"],[15,4,1,"","get_client"],[15,4,1,"","is_intact"],[15,4,1,"","out_dir"],[15,4,1,"","output"],[15,5,1,"","overwrite"],[15,4,1,"","run"],[15,5,1,"","save_to"]],"emu.pipeline.process":[[17,3,1,"","Downsample"],[17,3,1,"","NWB"],[17,3,1,"","PDilTask"],[17,2,1,"","gen_ncs"],[17,3,1,"","sEEGTask"]],"emu.pipeline.process.Downsample":[[17,5,1,"","channel_id"],[17,5,1,"","decimate"],[17,4,1,"","output"],[17,4,1,"","requires"],[17,4,1,"","run"],[17,4,1,"","save_path"]],"emu.pipeline.process.NWB":[[17,5,1,"","decimate"],[17,4,1,"","make_timeseries"],[17,4,1,"","output"],[17,4,1,"","requires"],[17,4,1,"","run"],[17,4,1,"","save_path"]],"emu.pipeline.process.PDilTask":[[17,5,1,"","data_root"],[17,4,1,"","patient_data"],[17,5,1,"","patient_id"]],"emu.pipeline.process.sEEGTask":[[17,4,1,"","ch_files"],[17,5,1,"","data_root"],[17,5,1,"","patient_id"],[17,4,1,"","sEEG_root"]],"emu.pipeline.remote":[[18,1,1,"","Patients"],[18,3,1,"","RemoteCSV"],[18,3,1,"","RemoteFile"],[18,3,1,"","RemoteNLX"],[18,3,1,"","RemotePatientManifest"],[18,3,1,"","RemoteStudyManifest"]],"emu.pipeline.remote.RemoteCSV":[[18,4,1,"","append"],[18,4,1,"","commit"],[18,5,1,"","file_id"],[18,5,1,"","file_path"],[18,4,1,"","load"]],"emu.pipeline.remote.RemoteFile":[[18,5,1,"","file_id"],[18,5,1,"","file_path"],[18,4,1,"","output"]],"emu.pipeline.remote.RemoteNLX":[[18,5,1,"","file_id"],[18,4,1,"","header"],[18,4,1,"","raw_header"]],"emu.pipeline.remote.RemotePatientManifest":[[18,4,1,"","generate_id"],[18,4,1,"","output"],[18,4,1,"","register_folder"],[18,4,1,"","register_study_root"]],"emu.pipeline.remote.RemoteStudyManifest":[[18,4,1,"","create"],[18,4,1,"","output"],[18,4,1,"","requires"],[18,5,1,"","study"]],"emu.pipeline.timestamps":[[19,3,1,"","ChannelTimestamp"]],"emu.pipeline.timestamps.ChannelTimestamp":[[19,5,1,"","channel_id"],[19,4,1,"","output"],[19,4,1,"","requires"],[19,4,1,"","run"],[19,4,1,"","save_path"]],"emu.pipeline.utils":[[20,3,1,"","TaskOutput"],[20,2,1,"","file_ids_by_channel"]],"emu.pipeline.utils.TaskOutput":[[20,4,1,"","keys"]],"emu.process_videos":[[21,2,1,"","add_end"],[21,2,1,"","add_start"],[21,1,1,"","get_url_params"],[21,2,1,"","preprocess"],[21,2,1,"","process"],[21,2,1,"","process_video"],[21,1,1,"","records"],[21,1,1,"","resolution_presets"],[21,1,1,"","trickshots"]],"emu.utils":[[22,1,1,"","DEFAULT_MANIFEST_FID"],[22,3,1,"","Experiment"],[22,1,1,"","RELEVANT_FILES"],[22,1,1,"","_get_block"],[22,1,1,"","_get_ch"],[22,1,1,"","_parse_ch"],[22,1,1,"","channel_fn_rgx"],[22,2,1,"","create_or_reuse_client"],[22,2,1,"","generate_id"],[22,2,1,"","get_file_manifest"],[22,2,1,"","get_file_type"],[22,2,1,"","is_url"],[22,2,1,"","load_patients"],[22,2,1,"","md5_16"]],"emu.utils.Experiment":[[22,4,1,"","__repr__"],[22,4,1,"","files"],[22,4,1,"","load_channels"]],emu:[[2,0,0,"-","auth"],[3,0,0,"-","backend"],[4,0,0,"-","cli"],[5,0,0,"-","download"],[8,0,0,"-","luigi"],[9,0,0,"-","meds"],[10,0,0,"-","names"],[11,0,0,"-","neuralynx_io"],[12,0,0,"-","nwb"],[13,0,0,"-","pdil"],[16,0,0,"-","pipeline"],[21,0,0,"-","process_videos"],[22,0,0,"-","utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","data","Python data"],"2":["py","function","Python function"],"3":["py","class","Python class"],"4":["py","method","Python method"],"5":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:data","2":"py:function","3":"py:class","4":"py:method","5":"py:attribute"},terms:{"0":[0,9,11,18,21,22,26,27],"00":[0,27],"000000":27,"0007":27,"03":0,"05":[0,27],"06":[0,27],"07":[0,27],"078367":27,"08":0,"083959":27,"09":0,"0j":27,"0x103e2ea50":26,"0x10bc37c10":[],"1":[0,9,11,15,26,27],"10":[12,26,27],"100":[26,27],"1000":[0,11,12],"1000000":11,"103":0,"11":27,"110800":27,"116":0,"12":[0,27],"123456":23,"128k":21,"13":27,"14":27,"146":27,"147":27,"148":27,"149":27,"15":[0,12,27],"150":[0,27],"1500":0,"16":[20,27],"17":27,"173":27,"174":27,"175":27,"176":27,"177":27,"178":27,"18":[0,27],"19":0,"19680801":26,"19it":27,"2":[0,24,27],"20":0,"2014":25,"2020":0,"21":0,"22":0,"222":27,"223":27,"225":27,"226":27,"227":27,"23":0,"25":9,"250":0,"2535":0,"256":27,"274455":27,"3":[0,27],"30":0,"300000":12,"3165165981":[],"3219390234":27,"33":0,"33428169":0,"34":0,"358413":27,"37":0,"38":0,"39it":27,"4":[0,22,26,27],"4000":[12,27],"4000hz":27,"419018":27,"43it":27,"45it":27,"49923281":27,"5":[0,9,15,26,27],"512":11,"519562":27,"52":0,"52it":27,"548549":27,"55":0,"562127657379":23,"564397":27,"568142":27,"56it":27,"57it":27,"581662":27,"588757437066":22,"588783":27,"6":[0,9,27],"60":[0,12],"628698648907":27,"628721484958":27,"628728186668":27,"629611688205":27,"629611713944":27,"629615908637":27,"629620274728":27,"6305":27,"633031167652":27,"667150":27,"7":[9,27],"70":0,"749":27,"750":[0,27],"750k":21,"751":27,"754":27,"755":27,"756":27,"757":27,"8":[0,12,27],"80":[0,9],"9":[22,27],"901004":27,"914512":27,"95":9,"951420":27,"96":[0,9],"967568":27,"98":9,"987":27,"\u00b5v":11,"case":7,"class":[0,1,27],"default":[7,18,25],"do":[7,25,26,27],"function":[1,25,27],"import":[0,23,26,27],"int":[3,18,27],"return":[0,7,9,15,17,18,19,22,27],"short":[7,10,23],"true":[0,7,10,11,17,20,21,27],"try":27,"var":27,A:[0,7,15,17,18,19],And:24,As:[0,26],At:25,But:26,By:7,For:[0,23,25,26],If:[7,15,17,18,19,25,27],In:[15,17,19,25],It:25,NOT:7,No:27,On:7,One:0,The:[7,15,17,18,19,23,25,27],There:[25,26],These:27,To:23,_0007:27,_:[14,22,27],__del__:[1,7],__enter__:[1,7],__exit__:[1,7],__name__:[1,15],__repr__:[1,15,22],__str__:[1,9],_cl:[0,1,9],_create_seeg_path:[1,15],_exists_and_is_dir:[1,7],_get_block:[1,22],_get_ch:[1,22],_ioncontext:26,_name_:[0,1,9],_parse_ch:[1,22],_taskoutput:[14,27],_tmax:[0,1,9],_vd:[0,1,9],_weight:[1,9],about:[25,26],abov:0,accept:25,accept_trailing_slash:[1,7],accept_trailing_slash_in_existing_dirpath:[1,7],access:[4,15,17,18,19],account:7,acquisit:27,across:27,add:[3,25],add_:26,add_behavior:[1,14],add_collabor:[1,3],add_electrod:[1,12],add_end:[1,21],add_start:[1,21],add_ttl:[1,12],addit:[7,15,17,19],address:3,adelphi:10,adf:27,administr:0,aeds:0,after:7,again:25,agamemnon:10,ahwahne:10,akagi:10,align:26,all:[7,15,17,18,19,25,27],all_fil:27,allow:25,alreadi:[7,25],also:[25,26],amt:0,an:[0,7,24],analogu:27,anat_lg:27,anat_sh:27,ani:[15,17,18,19,25],annotationseri:27,anoth:25,anschutz:12,antar:10,api:24,app:23,append:[0,1,18],ar:[0,7,15,17,18,19,27],arco:10,arg:[4,15,17,18,19,21,22],argument:3,ari:10,ariel:10,arrai:26,artemi:10,associ:[7,25],atomiclocalfil:7,atomicwrit:7,atomicwritableboxfil:[1,7],attribut:1,attributeerror:[],audio_bitr:21,auditori:25,augyn:10,aurora:10,australia:25,auth:[1,6,23,27],auth_config:7,authent:7,auto:[],autoapi:[],auxiliari:7,awai:7,ax:26,b:[0,7],backend:[1,6,27],bai:10,base:[0,7,9,14,15,17,18,19,20,22],baselin:0,basic:27,basl:0,beagl:10,been:27,befor:27,begin:26,behavior:[14,27],behavior_fil:27,behavior_raw_path:27,behaviorraw:[1,14,15,27],being:[25,27],bellerophon:10,bib:25,bibliographi:25,bibtex:25,bill:10,block:[14,22,24,25,27],blocknum_:14,blood:0,bodi:0,bonchun:10,book:[24,25,26],bool:[3,7,18],botani:10,both:[25,27],bounti:10,box:[1,6,8,14,15,25,27],box_fil:14,boxclient:[1,7,27],boxsdk:[3,27],boxtarget:[1,7,27],bozeman:10,brattain:10,brian:25,brisban:25,browser:23,build:[15,25,27],built:25,bundl:24,buran:10,c0:9,c:[0,1,9,27],cache_behavior:[1,14,27],cache_fp:[1,15,27],cache_nc:[1,14,27],cache_nev:[1,14,27],cachedata:[1,15],cachetaskoutput:[1,15],calcul:0,call:[7,25,27],can:[0,7,15,17,18,19,23,25,26],can_view_path:3,carolina:10,carri:7,cbe30338:0,cell:25,centaur:10,certain:7,ch:[17,27],ch_file:[1,17],ch_id:17,chan_num:27,channel:[22,27],channel_fn_rgx:[1,22],channel_id:[1,17,19,20],channeltimestamp:[1,19],check:[7,23,24,26],check_ncs_record:[1,11],check_or_cr:[1,15,27],chemic:0,christoph:25,cite:25,cl:[0,1,9,15],cl_dist:[1,9],classmethod:[9,15],clavin:10,clean:[1,15],clearanc:0,cli:[1,6],click_spinn:27,client:[7,22,23],clip_a:9,clip_b:9,close:[1,7],cloud:7,cm:26,cmap:26,cn:0,code:24,cognit:25,cold:26,collabor:3,collaborationrol:3,collect:27,collectionbuild:[1,15],color:26,colorado:12,column:27,com:23,combin:27,command:25,commit:[1,18],commonmark:25,compart:0,complet:[7,15,17,18,19],complex:25,compress:27,comput:[15,17,18,19,25],concat:[0,27],concentr:0,concord:10,concret:0,confer:25,config:23,consid:[15,17,18,19],constant:0,constel:10,constitut:10,contain:[0,24,27],content:[1,24,25],context:7,convert:27,convertinng:27,coolwarm:26,copernicu:10,cortex:25,count:[11,15,17,19],cp:0,cp_norm:0,creat:[0,1,7,12,15,17,18,19,23,26,27],create_administr:[0,1,9],create_nwb:[1,14,27],create_or_reuse_cli:[1,22],cred_fp:2,credenti:23,csc100_0007:27,csc101_0007:27,csc102_0007:27,csc103_0007:27,csc104_0007:27,csc105:27,csc105_0007:27,csc106_0007:27,csc107_0007:27,csc108_0007:27,csc109_0007:27,csc:[22,27],css:[1,9],csv:[0,27],custom_lin:26,cycler:26,d2_ncs_path:27,d2_ncs_task:27,d2_nev:27,d:[0,14,25,27],da:0,dai:[0,27],dat_fil:17,data:[0,4,12,26,27],data_interfac:27,data_root:[1,15,17],data_time_len:12,data_typ:[15,18],databas:[15,17,18,19],datafram:[0,27],date:0,datetim:27,dc:0,dd:27,de:25,decim:[1,17],declar:[15,17,19],decor:7,def:[0,7,27],default_config:[1,2],default_config_fp:[1,7],default_manifest_fid:[1,22,27],default_root:[1,2,27],defiant:10,defin:[25,27],deleg:7,depend:[7,15,17,18,19,25],deriv:0,desc:[12,14,27],descend:7,describ:[0,15,17,19],design:7,desir:7,destin:7,destini:10,determin:[7,15,17,18,19],dev:27,develop:24,devic:12,df:[0,12,15,17,18,19,21],dict:[15,17,18,19],differ:25,dilut:0,dir:23,dir_path:15,directli:[23,25],directori:[7,23],displai:25,distribut:0,dl_file:[1,5],do_compress:27,doc:25,document:[25,26],doe:[7,15,17,18,19],doesn:[7,25],dollar:26,don:[15,17,18,19],done:[15,17,18,19],dose:[0,9],down:23,download:[1,4,6,14,16,23,27],download_as_byt:[1,7],download_to:23,download_to_tmp:[1,7],downsampl:[1,17],drake:10,drop:0,dropbox:7,drug:[0,1,9],drugadministr:[0,1,9],dry_run:15,dt:0,dtype:12,dtypeconversionwarn:27,e:24,each:[0,15,17,19,27],eagl:10,ecephi:27,ecosystem:25,edit:7,editor:3,either:7,electrical_seri:27,electricalseri:27,electrod:[12,27],electrode_loc:[12,27],electrophysiolog:[1,14,27],elijahc:[0,27],elkin:10,els:[23,27],email:3,emb:26,emu:[0,1,25,27],emu_p38:27,enabl:7,end:[7,21,26,27],endeavour:10,ensur:27,enter:7,enterpris:10,entir:25,ephi:27,equat:0,equinox:10,escap:26,estimate_record_count:[1,11],etc:26,even:7,event:[1,14,27],event_delta:27,events_0007:27,everi:27,evid:25,ewm:0,exampl:[0,25,26],exc:7,exc_typ:7,excalibur:10,excelsior:10,except:7,exist:[1,7,15,17,18,19,23,25,27],exit:7,expandus:27,experi:[1,22],experimentmanifest:[1,15,27],extens:25,externaltask:18,extract:27,extract_trial_tim:[1,14],f:[0,1,9],fals:[3,7,9,12,14,15,18,21,22,27],fearless:10,federation_starship:[1,10],fetch:27,few:[15,17,19,23],fid:[7,11],fig:26,figsiz:26,file:[1,7,12,14,15,22,23,27],file_id:[1,5,7,15,18,23,27],file_id_to_path:[1,7,27],file_ids_by_channel:[1,20,27],file_info:23,file_manifest:20,file_nam:[1,15,27],file_path:[1,11,18,27],filealreadyexist:7,fileid:4,filemanifest:[1,15,27],filenam:[5,14,15,22,27],filepath:20,filesystem:7,filesystemexcept:7,filesystemtarget:7,finish:[15,17,18,19],firebrand:10,first:25,firstnam:[18,22],fix:26,flavor:25,float16:[12,27],float32:12,flow:0,flowrat:0,fn:27,folder:[1,3,7,22,23,27],folder_app:[1,3],folder_id:[7,18,23],folder_id_to_path:[1,7],folder_info:23,folder_path:7,follow:25,forc:[15,18],form:[0,23],format:[0,7,27],fp:[12,27],fp_list:17,frac:0,from:[0,7,12,14,15,18,23,26,27],from_datafram:[1,15],frontal:27,frontier:25,fs:[1,7,12,27],full:23,full_nam:10,full_warning_msg:27,func:[7,18],gallico:10,game:27,gander:10,gang:10,gen_nc:[1,15,17],gen_nlx_chunk:[1,14],gen_norm_dist:[1,9],gener:[7,27],generate_id:[1,18,22],get:[23,27],get_channel_id:[1,12,27],get_cl:[1,9],get_client:[1,15],get_data_manifest:[1,14],get_file_manifest:[1,3,22,27],get_file_typ:[1,22],get_folder_fil:27,get_url_param:[1,21],github:0,glob:27,gov:0,grab:23,greyhound:10,grissom:10,group:3,group_col:12,grp:12,guid:26,ha:[0,7,23,25],hathawai:10,hattera:10,have:[23,27],hdfstarget:7,hdhpk14:25,hdmf:27,head:[0,27],header:[1,18],header_length:[1,11],heer:25,helin:10,help:3,helper:[23,27],hera:10,here:[24,25,26],herm:10,hispaniola:10,hold:0,holdgraf:25,holdgraf_evidence_2014:25,home:[0,27],honshu:10,hood:10,horatio:10,horizon:10,hornet:10,hot:26,hour:0,how:24,hr:0,html:[0,26],http:0,hue:0,human:[14,25],huron:10,i:[23,27],id:[3,27],iff:[15,17,18,19],ignore_warn:17,ii:26,imag:26,implement:[7,15,17,18,19,27],implicitli:7,in_fil:21,includ:[25,26],index:[0,14],infil:21,info:[1,4],inform:[25,26],init:25,initi:[7,23],initialize_nwb:[1,12],inlet:0,inlin:0,input:25,insert:25,insid:[7,25],instanc:[15,17,18,19,23],instead:7,institut:12,int32:27,integr:0,interact:26,intern:25,interv:[0,9],intparamet:[15,17,19],intrepid:10,intro:25,io:[0,27],ion:26,ipykernel_1736:[],ipykernel_21877:27,ipykernel_4121:27,ipynb:25,is_intact:[1,15],is_url:[1,22],isdir:[1,7],iter_ncs_to_timeseri:[1,12],iterrow:27,its:[7,25,27],jckantor:0,job:15,join:27,json:23,jtnrvl8d6hd01616xysk3g1h0000gn:27,jupyt:[25,26],jupytext:25,jwt:[1,2,23,27],k:27,kearsarg:10,keep:26,kei:[1,15,17,19,20,27],kelvin:10,kernel:25,keypress1:27,keypress2:27,keypress3:27,keypress4:27,keypress5:27,keypress:27,kg:0,kind:25,knight:25,kongo:10,korolev:10,kwarg:[3,4,15,17,18,19,21,22],kyushu:10,l:[0,27],la_:26,lab:12,label_blockstart:[1,12],lacosamid:[1,9],lalo:10,lamotrigin:[0,1,9],languag:25,lantre:10,last:27,lastnam:[18,22],legend:26,len:27,less:[7,25],level:0,levetiracetam:[0,1,9],lexington:10,lfp:27,lib:27,liber:10,like:[7,15,25],line2d:26,line:[25,26],lineplot:0,linspac:[0,26],list:[1,3,15,17,18,19,27],livingston:10,ll:[23,25,27],load:[1,15,18,27],load_all_nev:[1,14],load_channel:[1,22],load_game_data:[1,14,27],load_nc:[1,11,27],load_nev:[1,11,27],load_pati:[1,22],load_pdil_ev:[1,14,27],load_tim:11,local:[7,27],local_path:7,local_schedul:[14,27],localtarget:7,locat:[7,12],lof:27,logger:[1,7],logspac:26,look:[7,25],lot:26,luigi:[1,6,14,15,17,18,19,27],lw:26,m:0,magellan:10,magic:7,mai:3,main:[1,4],majest:10,make:[0,26],make_timeseri:[1,17],malinch:10,manag:[7,27],mani:[0,25],map:12,markedli:25,marker:0,markup:25,mass:0,mat:[14,27],mat_path:27,math:26,matplotlib:[0,26],max:0,mayflow:10,mbox:26,mc:24,md5_16:[1,22],md:[25,27],mdict:27,mean:[0,26],med:[0,1,6],medic:0,medium:26,mekong:10,member:[15,17,19],merrimac:10,metaclass:[15,17,19],metadata:[23,25],method:[0,7,15,17,18,19,23],mg:0,microvolt_sc:[1,11],might:[15,17,18,19],millivolt_sc:[1,11],misc:27,miss:27,missing_task:27,missingparentdirectori:7,mixer:0,mkdir:[1,7],mod:27,mode:7,model:0,modul:[1,27],modulenotfounderror:27,more:[24,25,26],moreov:25,most:[25,27],move:7,move_to_final_destin:[1,7],muleskinn:10,multilin:10,multipl:[15,17,18,19],must:[15,17,18,19,25],mv:11,my:25,mydirectivenam:25,myfilesystemtarget:7,mytask:[7,15,17,19],n:[0,11,25,26,27],name:[0,1,6,25,27],nameerror:27,nan:27,nash:10,nautilu:10,nb:25,nc:[12,14,15,22,27],ncbi:0,ncs_fp:[12,14],ncs_path:[12,14,27],ncs_record:[1,11],ncs_samples_per_record:[1,11],ncs_to_grp_eseri:[1,12],ncs_to_nwb:[1,12],ncs_to_nwb_raw:[1,12,27],ncs_to_timeseri:[1,12],nebula:10,necessari:7,need:[15,17,18,19,23],neuralynx:[12,27],neuralynx_io:[1,6,27],neurosci:25,nev:[1,14,15,27],nev_as_record:[1,11,27],nev_fp:[12,14,27],nev_path:[12,27],nev_record:[1,11],nev_to_behavior_annot:[1,12],nih:0,nlm:0,nlx:27,nlx_to_nwb:[1,12,27],nlxraw:[1,14,15,27],nobl:10,non:[0,15,17,19],none:[7,9,11,12,14,15,18,21,22],nop:7,norkova:10,normal:[0,9],northridg:10,note:[7,15,17,18,19,24,25],notebook:25,notifi:3,nova:10,np:[0,12,26,27],num_practice_tri:12,num_trial:12,numpi:[0,26,27],nwb:[1,6,17,27],nwb_path:27,nwb_to_mat:27,nwbfile:[12,27],nwbhdf5io:27,oberth:10,obj:7,obj_to_path:[1,7],object:[0,3,7,9,14,15,20,22,27],objectmapp:27,odeint:0,odin:10,odyssei:10,onc:25,one:25,onli:[7,15,17,18,19,25],op:27,open:[1,7,23],oper:7,option:7,orbit:27,order:18,orinoco:10,os:27,other:[15,17,18,19],otherwis:[7,15,17,18,19],out:[7,24,26],out_dir:[1,15],out_fil:21,out_mat:27,outcom:27,outlet:0,output:[1,7,15,17,18,19,25,27],output_path:7,overrid:[15,17,18,19],overridden:[15,17,19],overwrit:[1,15],p:[22,27],packag:[1,27],page:[24,25],panda:[0,27],par:27,param1:15,param2:15,param:[0,7],paramet:[0,3,7,15,17,18,19],parent:7,parse_func:18,parse_head:[1,11],parse_neuralynx_time_str:[1,11],particip:[1,14,27],paslei:25,pasteur:10,path:[7,12,18,23,25,27],path_to_config:7,path_to_fid:[1,7],path_to_obj:[1,7],path_to_root:[1,7],pathlib:7,patient:[0,1,18,27],patient_data:[1,17],patient_id:[1,4,14,15,17,22,27],patient_ord:18,patientsloc:[1,15],pattern:25,payoff_dict:[1,14],pd:[0,18,27],pdil:[1,6,27],pdiltask:[1,17,27],per:0,percent:0,pharmacokinet:0,pipelin:[1,6,24],pk:0,plasma:0,plot:[1,9,26],plot_cp:[1,9],plt:[0,26],po_day_02:27,po_day_02_raw:27,pod2:27,pod4:27,points_to_choic:[1,14,27],post:[26,27],potemkin:10,power:25,practice_incl:[12,14],pre:25,predict:25,pregabalin:[0,1,9],preprocess:[1,4,21],preset:21,print:[25,27],problem:7,process:[1,6,16,19,21,27],process_video:[1,6],produc:[15,17,18,19],prog_bar:[3,22],prometheu:10,prop_cycl:26,properli:25,properti:[7,9,15,17,19],provid:27,proxima:10,psych:27,pt01_blocknum_1_computertt_coop_taskoutput:27,pt01_blocknum_2_humantt_coop_taskoutput:27,pt01_blocknum_3_computertt_defect_taskoutput:27,pt01_blocknum_4_humantt_defect_taskoutput:27,pt01_blocknum_5_humantt_coop_taskoutput:27,pt01_blocknum_6_computertt_coop_taskoutput:27,pt01_practice_blocknum_0:27,pt6305:27,pt:[0,14],pt_01:27,pt_01_postopday2_pdil:27,pt_01_postopday4_pdil:27,pt_6305:27,pt_manifest_file_id:22,pubm:0,pueblo:10,pull:23,purpos:25,py:27,pyenv:27,pynwb:27,pyplot:[0,26],python3:27,python:27,q:0,queri:0,r:[7,27],rais:7,raise_if_exist:7,ramsai:25,randn:26,random:26,rang:26,rate:0,raven:10,raw:[1,6,13,15,27],raw_fil:[14,27],raw_hdr:11,raw_head:[1,18],raw_path:14,rcparam:26,reactor:0,read:[1,7],read_csv:[0,18],read_head:[1,11],read_record:[1,11],readabl:[1,7],readableboxfil:[1,7],reason:7,recent:27,record:[1,11,21],record_dtyp:11,record_skip:11,recurs:7,refer:[24,25],regimen:0,regist:[15,17,19],register_fold:[1,18],register_study_root:[1,18],regular:25,rel:[0,25],relevant_fil:[1,22],reliant:10,reload:18,remot:[1,6,16,27],remotecsv:[1,18,27],remotefil:[1,18],remotenlx:[1,18],remotepatientmanifest:[1,18,27],remotestudymanifest:[1,18],remov:[1,7],rename_dont_mov:7,render:25,render_screen1:27,render_screen2:27,render_screen4:27,render_screen5:27,renegad:10,repr:22,repres:7,represent:15,reproduc:26,republ:10,repuls:10,requir:[1,15,17,18,19],rescale_data:11,research:24,reset_index:0,resolut:21,resolution_preset:[1,21],resourc:[15,17,18,19],rest:25,result:25,retrn:27,rever:10,rgx_string:14,right:7,robert:25,role:3,rolenam:25,row:[18,27],rpt:27,rubicon:10,run:[1,7,15,17,18,19,25],run_some_external_command:7,rutledg:10,s:[23,24,25,26,27],same:[0,15,17,18,19,25,27],sampl:[24,26],saratoga:10,save_path:[1,17,19],save_to:[1,15,27],savemat:27,scipi:[0,27],scovil:10,screen:27,seaborn:0,seaquest:10,seaview:10,second_param:[15,17,19],see:[15,17,18,19,24,25,26],seed:26,seeg:27,seeg_raw_path:[14,27],seeg_root:[1,17,27],seegtask:[1,17,19],seekabl:[1,7],self:[7,9,14,15,17,18,19,20,22,27],sent:27,sentinel:10,separ:0,seri:0,serv:25,server:[18,23],set_baselin:[0,1,9],sex:14,sha1:[1,15],shape:27,shepard:10,shirkahr:10,should:[15,17,18,19,27],show:10,show_cl:[1,9],show_vd:[1,9],sign:26,signal_sc:11,silversid:10,similar:[23,25],simpl:[0,4],simplest:25,sinc:[0,15,17,18,19],singl:[0,14,15,17,18,19,27],sio:27,sitak:10,site:27,skip_trash:7,slight:25,slow:21,small:25,sn:0,so:[7,25],solv:7,some:[25,26],some_fil:7,somewher:23,sort:27,span:[9,25],spec:27,speci:[0,14],specif:25,specifi:[7,27],sphinx:25,split:27,squeez:20,src:[23,27],stack:27,stand:25,stargaz:10,start:21,startswith:27,stat:0,state:[0,26],steadi:0,step:7,stir:0,store:[0,23,25,27],str:[3,7,9,18],straight:23,strata:10,streamlin:23,string:[3,10],struct_as_record:14,struct_nam:20,structur:25,studi:[1,14,15,18,22,27],study_pdil:27,subclass:[7,15,17,18,19],submodul:1,subpackag:1,subplot:26,suffix:21,summari:23,support:7,sure:26,sync:27,syntax:[23,25],syracus:10,system:7,t:[0,7,9,15,17,18,19,25,26,27],tabul:27,tank:0,target:[7,15,17,18,19],task:[7,14,15,17,18,19,27],taskoutput:[1,14,20],taskoutput_meta:[1,14],temp:27,temp_output_path:7,temporari:7,temporary_fil:[1,7],temporary_path:[1,7],tex:26,text:[0,25],thei:[7,15,17,18,19,25],them:[7,27],thi:[7,15,17,18,19,23,24,25,26],thing:27,thompson:12,those:25,threshold:12,thrown:7,thunderchild:10,tic:27,time:[0,9,25,27],time_delta:0,time_str:11,timeseri:27,timestamp:[1,6,14,16,27],titan:10,titl:0,tmax:[1,9],tmax_dist:[1,9],tmp:27,to_datafram:27,to_nwb:[1,14],toc:27,token:7,tolist:0,tombaugh:10,tool:25,toolbox:27,total:0,tqdm:27,tqdm_notebook:27,trace:27,traceback:[7,27],trial:27,trial_start:27,trickshot:[1,21],triest:10,trim_buff:12,trode:12,truncnorm:0,ts_file:17,tt_:14,ttl:[1,14,27],ttl_delta:27,two:25,txt:7,type:27,typer:[3,27],typic:7,u:[0,1,9],uint32:27,unicod:3,uniqu:[0,27],unit:[0,15,17,19],univers:12,unnam:27,upload:[1,7,23,27],url:[22,23],us:[0,7,23,27],usag:7,user:[0,3],user_ag:7,uss:10,util:[1,6,16,27],v:[0,11],valiant:10,valid:[7,25],valu:[10,15,17,18,19,27],var_kei:14,variat:25,vd:[1,9],vd_dist:[1,9],ventur:10,verbos:[4,14,21,27],veri:25,version:27,via:23,victori:10,video_bitr:21,video_directori:21,video_set:21,volga:10,volt_scal:[1,11],volum:0,volumetr:0,voyag:10,w:[7,14,27],wa:7,wai:7,want:[23,26],warn:27,wb:23,we:[0,27],weight:[0,9],well:[23,26,27],wendi:25,when:[7,25],where:[0,27],wherea:[7,25],whether:25,which:[7,15,17,19,25,27],whose:[15,17,18,19],wire:27,wire_9_electrode_6:27,wire_num:[12,27],within:[0,7],work:[15,17,18,19,23,25,26],worker:[15,17,18,19,27],wrap:27,writabl:[1,7],write:[7,25,27],writeabl:7,written:[7,25],wt:9,x:0,y:0,yamato:10,yield:[14,15,27],yorktown:10,you:[15,17,18,19,23,25,26,27],your:[15,17,18,19,23,26],zip:0},titles:["AED Load","API documentation","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.auth</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.backend</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.cli</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.download</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.luigi.box</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.luigi</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.meds</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.names</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.neuralynx_io</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.nwb</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pdil</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pdil.raw</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline.download</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline.process</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline.remote</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline.timestamps</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.pipeline.utils</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.process_videos</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">emu.utils</span></code>","emu Box SDK","EMU Documentation","Markdown Files","Content with notebooks","Pipeline preprocessing example"],titleterms:{"class":[7,9,14,15,17,18,19,20,22],"function":[2,3,4,5,7,9,10,11,12,14,15,17,20,21,22],AED:0,access:23,ad:25,api:1,ar:25,attribut:[2,3,7,10,11,14,18,21,22],auth:2,backend:3,block:26,box:[7,23],citat:25,cli:4,code:[25,26],content:[2,3,4,5,7,9,10,11,12,14,15,17,18,19,20,21,22,26],data:23,dilemma:24,direct:25,document:[1,24],download:[5,15],emu:[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],exampl:27,execut:25,file:25,load:0,luigi:[7,8],markdown:[25,26],med:9,modul:[2,3,4,5,7,9,11,12,14,15,17,18,19,20,21,22],myst:[25,26],name:10,neuralynx_io:11,notebook:26,nwb:12,output:26,packag:10,pdil:[13,14,24],pipelin:[15,16,17,18,19,20,27],preprocess:27,prison:24,process:17,process_video:21,raw:14,refer:[],remot:18,role:25,sdk:23,submodul:[6,8,13,16],subpackag:6,timestamp:19,us:25,util:[20,22],what:25,your:25}})