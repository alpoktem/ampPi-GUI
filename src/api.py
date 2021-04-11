from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

pdsendpath = "/usr/bin/pdsend"

effects = {1:"Clean", 2:"Chorus", 3:"Warble Chorus", 4:"Tremolo", 5:"Vibrato", 6:"Wah", 7:"Ring Modulator", 8:"Low Fuzz Wah", 9:"Med Fuzz Wah", 
           10:"Hi Fuzz Wah", 11:"Ring Mod Fuzz", 12:"Fuzz", 13:"Subtractive OD", 14:"Tube Screamer", 15:"Digital Delay", 16:"Tape Echo"}

preset = 1

@app.get('/')
def read_form(request: Request):
    #Open default preset
    os.system("echo '0 "+ str(preset) +";' | "+ pdsendpath +" 5000 localhost")

    return templates.TemplateResponse('amppi.html', context={'request': request, 'effects':effects, 'active':preset})

@app.post('/')
def read_form(request: Request, effect: int = Form(...)):
    #Close current effect
    global preset
    os.system("echo '1 "+ str(preset) +";' | "+ pdsendpath +" 5000 localhost")

    #Open new effect
    preset = effect
    os.system("echo '0 "+ str(preset) +";' | "+ pdsendpath +" 5000 localhost")

    return templates.TemplateResponse('amppi.html', context={'request': request, 'effects':effects, 'active':preset})
