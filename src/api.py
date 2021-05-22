from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
import csv

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

pdbinpath = os.getenv('PD_BIN_PATH') or "/usr/bin"
pdsendpath = os.path.join(pdbinpath, "pdsend")

print("pdsendpath", pdsendpath)

# effects = {"1":"Clean", "2":"Chorus", "3":"Warble Chorus", "4":"Tremolo", "5":"Vibrato", "6":"Wah", "7":"Ring Modulator", "8":"Low Fuzz Wah", "9":"Med Fuzz Wah", 
#            "10":"Hi Fuzz Wah", "11":"Ring Mod Fuzz", "12":"Fuzz", "13":"Subtractive OD", "14":"Tube Screamer", "15":"Digital Delay", 
#            "16":"Bold as love", "17":"Chorus", "18":"Down the stairs", "19":"Looper", "20":"Phaser", "21":"Reverb", "22":"Ring modulator",
#            "23":"Simple delay", "24":"Simple fuzz", "25":"Step-vibrato", "26":"Synth", "27":"The Hexxciter", "28":"Tremolo", "29":"Vibrato", "30":"WhaAuto"}
effects = {}

effects_dir = os.getenv('EFFECTS_DIR')
effects_config = os.getenv('EFFECTS_CONFIG')

preset = "1"

@app.get('/')
def read_form(request: Request):
    #Open default preset
    global preset
    os.system("echo '0 "+ preset +";' | "+ pdsendpath +" 5000 localhost")
    return templates.TemplateResponse('amppi.html', context={'request': request, 'effects':effects, 'active':preset})

@app.post('/')
def change_preset(request: Request, effect: str = Form(...)):
    #Close current effect
    global preset
    os.system("echo '1 "+ preset +";' | "+ pdsendpath +" 5000 localhost")
    print("echo '1 "+ str(preset) +";' | "+ pdsendpath +" 5000 localhost")

    #Open new effect
    preset = effect
    os.system("echo '0 "+ preset +";' | "+ pdsendpath +" 5000 localhost")
    print("echo '0 "+ preset +";' | "+ pdsendpath +" 5000 localhost")

    return templates.TemplateResponse('amppi.html', context={'request': request, 'effects':effects, 'active':preset})

@app.on_event("startup")
async def startup_event():
    global effects
    with open(effects_config, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row['load'] == '#':
                effects[row['id']] = row['name']

    print(effects)
    print("%i effects"%len(effects))
