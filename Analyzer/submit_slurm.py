import os
from CP3SlurmUtils.Configuration import Configuration as CP3SlurmConfiguration
from CP3SlurmUtils.SubmitWorker import SubmitWorker as slurmSubmitWorker

def submit_slurm(f,fjobxml,output,nmax,pdf,run,toprec):

    workdir = os.path.join(os.getcwd(), "slurm")

    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    cfg = CP3SlurmConfiguration()

    ### configure where all the slurm files (submit, logs) go
    cfg.sbatch_workdir = workdir # where to run the scripts from
    cfg.inputSandboxDir = os.path.join(workdir, "input") # where to put the inputs (if any)
    cfg.batchScriptsDir = workdir # where to put the slurm scripts
    cfg.batchScriptsFilename = "slurmSubmission.sh"
    cfg.sbatch_partition = 'Def'
    cfg.sbatch_qos = 'normal'
    ### stageout, move the output files somewhere (optional, can be disabled by settings 'cfg.stageoutFiles = []'
    cfg.stageoutFiles = ["*.root"]
    cfg.stageoutDir = os.path.join(workdir, "out", "${SLURM_ARRAY_TASK_ID}") # where to move the outputs (here : 'out/X, can also be a single path)
    cfg.stageoutLogsDir = os.path.join(workdir, "logs")
    ### CPU time and memory
    cfg.sbatch_time = "0-10:00"
    cfg.sbatch_mem = "10000"
    ### the interesting part
    cfg.useJobArray = True
    cfg.payload = "cd /home/ucl/cp3/swuycken/scratch/CMSSW_10_5_0/src/tHGG/Analyzer/; python read.py --nmax=%s --pdf=%s --run=%s --toprec=%s --sample=${sample} --xml=${fjobxml} --output=${output}"%(nmax,pdf,run,toprec)
    cfg.inputParamsNames = ["sample", "fjobxml","output"]
    cfg.inputParams = []
    cfg.inputParams.append([f,fjobxml,output])


    slurm_submit = slurmSubmitWorker(cfg, submit=True,yes=True)
    slurm_submit()
