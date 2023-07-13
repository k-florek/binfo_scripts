#!/usr/bin/env python3

import os,sys
import csv

from pypdf import PdfWriter
from pypdf.generic import BooleanObject, NameObject, IndirectObject, NumberObject


path_PDF = sys.argv[1]
path_CSV = sys.argv[2]

def mergeData(d):
    screeningData = {
                    'Candidate Name':d['Name'], 
                    'PVLNum':"", 
                    'Department': '',
                    'EducationA': '/Yes' if d['Education'] == 'a' else '/Off', 
                    'EducationB': '/Yes' if d['Education'] == 'b' else '/Off', 
                    'EducationC': '/Yes' if d['Education'] == 'c' else '/Off', 
                    'EducationNA': '/Yes' if d['Education'] == 'n' else '/Off', 
                    'TrainingA': '/Yes' if d['Training'] == 'a' else '/Off', 
                    'TrainingB': '/Yes' if d['Training'] == 'b' else '/Off',
                    'TrainingC': '/Yes' if d['Training'] == 'c' else '/Off',
                    'TrainingNA':'/Yes' if d['Training'] == 'n' else '/Off',
                    'JobExpA': '/Yes' if d['RelevantJobExperience'] == 'a' else '/Off', 
                    'JobExpB': '/Yes' if d['RelevantJobExperience'] == 'b' else '/Off',
                    'JobExpC': '/Yes' if d['RelevantJobExperience'] == 'c' else '/Off',
                    'JobExpNA': '/Yes' if d['RelevantJobExperience'] == 'n' else '/Off',
                    'SupExpA': '/Yes' if d['SupervisoryExperience'] == 'a' else '/Off', 
                    'SupExpB': '/Yes' if d['SupervisoryExperience'] == 'b' else '/Off',
                    'SupExpC': '/Yes' if d['SupervisoryExperience'] == 'c' else '/Off',
                    'SupExpNA': '/Yes' if d['SupervisoryExperience'] == 'n' else '/Off',
                    'TechSkillsA': '/Yes' if d['Technical Skills'] == 'a' else '/Off', 
                    'TechSkillsB': '/Yes' if d['Technical Skills'] == 'b' else '/Off',
                    'TechSkillsC': '/Yes' if d['Technical Skills'] == 'c' else '/Off',
                    'TechSkillsNA': '/Yes' if d['Technical Skills'] == 'n' else '/Off',
                    'LeadershipA': '/Yes' if d['LeadershipSkills'] == 'a' else '/Off', 
                    'LeadershipB': '/Yes' if d['LeadershipSkills'] == 'b' else '/Off',
                    'LeadershipC': '/Yes' if d['LeadershipSkills'] == 'c' else '/Off',
                    'LeadershipNA': '/Yes' if d['LeadershipSkills'] == 'n' else '/Off',
                    'Overall':d['OverallEvaluation'], 
                    'Strengths':d['Strengths'], 
                    'Weaknesses':d['Weaknesses'],  
                    'DNA': '/Yes' if d['Advance'] == 'no' else '/Off', 
                    'AWR': '/Yes' if d['Advance'] == 'maybe' else '/Off', 
                    'Adv': '/Yes' if d['Advance'] == 'yes' else '/Off'
                    }
    return screeningData

def lock_form_fields(page):
    """
    Locks all form fields on the given PyPdf2 Page object
    """
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].get_object()
        if writer_annot.get('/T'):
            writer_annot.update({
                NameObject("/Ff"): NumberObject(1)
            })

with open(path_CSV,'r') as inCSV:
    #read in csv data
    csvReader = csv.DictReader(inCSV, delimiter=',')
    for row in csvReader:
        #initialize pdf writer object
        writer = PdfWriter()
        writer.append(path_PDF)
        
        #format data for pdf form
        screeningData = mergeData(row)

        #update the fields and lock the forms
        for page in writer.pages:
            writer.update_page_form_field_values(page,screeningData)    
            lock_form_fields(page)

        #write pdf output
        fileName = f"{row['Name']}_PVL277789_Screening.pdf".replace(' ','_')
        with open(fileName, 'wb') as outPDF:
            writer.write(outPDF)
