from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferLogs=True
config.General.requestName = 'REQUESTNAME'
config.section_('JobType')
config.JobType.psetName = 'flashggAnalysisNtuplizerWithSyst_cfg.py'
config.JobType.pluginName = 'Analysis'
#config.JobType.inputFiles = ['']
config.JobType.pyCfgParams = ['year=2017','doSystematics=0']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.splitting='FileBased'
#config.Data.totalUnits = -1
config.Data.totalUnits = 2
config.Data.unitsPerJob = 2

config.Data.allowNonValidInputDataset = True
config.Data.publication = False
config.Data.inputDataset = 'INPUTDATASET'
config.Data.inputDBS = 'phys03'
config.Data.outputDatasetTag = 'PUBLISHDATANAME'
config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter'
config.Data.outLFNDirBase = 'OUTLFN'

config.section_('User')
config.User.voGroup = 'becms'
config.section_('Site')
config.Site.storageSite = 'T2_BE_IIHE'
