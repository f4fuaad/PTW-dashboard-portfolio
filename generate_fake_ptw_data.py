"""
PTW Register – Fake Data Generator
====================================
Generates a fully synthetic Permit to Work dataset
matching the structure of a real LNG construction PTW register.

No real names, companies, equipment tags, or project identifiers are used.
All data is randomly generated for portfolio / demonstration purposes.

Usage:
    pip install faker openpyxl pandas
    python generate_fake_ptw_data.py
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

STATUS_GROUP   = ['PROCESSING', 'SUSPENDED', 'CLOSED', 'REJECTED', 'ACTIVE']
PERMIT_STATUS  = ['Reviewed', 'Approved', 'Issued', 'Closed', 'Rejected', 'Suspended', 'Received']
RISK_RATINGS   = ['Low Risk', 'Medium Risk', 'High Risk']
PERMIT_TYPES   = ['Hot Work', 'Cold Work', 'Excavation', 'Electrical',
                  'Confined Space', 'Radiography', 'Lifting Operations']
COMPANIES      = ['AlphaEPC Co.', 'BetaConstruct Ltd.', 'GammaTech JV',
                  'Delta Engineering', 'Epsilon Contractors', 'Zeta Works']
DEPARTMENTS    = ['Construction', 'Commissioning', 'Mechanical', 'Electrical',
                  'Instrumentation', 'Civil', 'HSE', 'Piping', 'Structural']
SITES          = ['LNG Plant – EPC Zone 1', 'LNG Plant – EPC Zone 2',
                  'Utility Block – Zone A', 'Offsite – Lot W1/W2']
SECTIONS       = ['Process Train A (Tr-1)', 'Process Train B (Tr-2)',
                  'Utilities Block', 'Condensate Area', 'Flare System',
                  'Steam Generation Unit', 'Desalination Area', 'Oily Water Treatment']
AREAS          = ['Pipe Rack (LNG Train)', 'Electrical Building Area',
                  'Compressor Area', 'Storage Tank Farm', 'Heat Exchanger Bay',
                  'Control Room Area', 'Substation Area', 'Metering Station']
UNITS          = ['Main Pipe Rack East – Common Layer', 'Condensate Polisher Area',
                  'Cooling Water Pump Station', 'Instrument Air System',
                  'Emergency Diesel Generator']
OWNERSHIP      = ['Construction', 'Commissioning', 'Operations']
ACTUAL_AREAS   = ['PROCESS TR-01', 'PROCESS TR-02', 'UTILITY', 'DESALINATION AREA',
                  'OFFSITE', 'FLARE AREA', 'COMPRESSOR AREA', 'STORAGE AREA']
STATUSES_COL   = ['Approved', 'Closed', 'Suspended', 'Active', '']

def rand_ptw_number(permit_type):
    prefix = {'Hot Work':'HWP','Cold Work':'CWP','Excavation':'EXP',
               'Electrical':'ELP','Confined Space':'CSP',
               'Radiography':'RDP','Lifting Operations':'LOP'}.get(permit_type,'PTW')
    return f"{prefix}{random.randint(1000,19999)}"

def rand_date(start='2024-01-01', end='2026-03-01'):
    s = datetime.strptime(start,'%Y-%m-%d')
    e = datetime.strptime(end,'%Y-%m-%d')
    return s + timedelta(days=random.randint(0,(e-s).days))

def fmt_dt(d, time=True):
    if d is None: return None
    return d.strftime('%d-%m-%Y %H:%M') if time else d.strftime('%d-%m-%Y')

def maybe(val, prob=0.7):
    return val if random.random() < prob else None

rows = []
for i in range(600):
    pt  = random.choice(PERMIT_TYPES)
    co  = random.choice(COMPANIES)
    dep = random.choice(DEPARTMENTS)
    rd  = rand_date()
    sd  = rd + timedelta(days=random.randint(1,5))
    vf  = sd; vt = vf + timedelta(days=random.randint(1,30))
    rev = rd + timedelta(hours=random.randint(2,48))
    con = rev + timedelta(hours=random.randint(1,12))
    apr = con + timedelta(hours=random.randint(1,6))
    iss = apr + timedelta(hours=random.randint(1,4))
    rec = iss + timedelta(hours=random.randint(0,2))
    clo = maybe(rec + timedelta(days=random.randint(1,15)), 0.5)

    rows.append({
        'Sl. No': i+1,
        'STATUS by Group': random.choice(STATUS_GROUP),
        'Permit STATUS': random.choice(PERMIT_STATUS),
        'PTW Number': rand_ptw_number(pt),
        'Previous PTW Number': maybe(rand_ptw_number(pt), 0.3),
        'Risk Rating': random.choice(RISK_RATINGS),
        'Type of Permit': pt,
        'IDC (LOTO)': maybe(f"IDC{random.randint(1000,9999)}", 0.3),
        'EXCA': maybe(f"EXCA{random.randint(100,999)}", 0.15),
        'WAH': maybe(f"WAHC{random.randint(1000,9999)}", 0.25),
        'Grating Removal': maybe('Yes', 0.1),
        'Critical Lift': maybe('Yes', 0.1),
        'CSEC': maybe(f"CSEC{random.randint(1000,9999)}", 0.12),
        'Radiography': maybe('Yes', 0.05),
        'Bypass': maybe('Yes', 0.08),
        'Other Forms': maybe('Yes', 0.1),
        'Site': random.choice(SITES),
        'Section': random.choice(SECTIONS),
        'Area': random.choice(AREAS),
        'Unit': random.choice(UNITS),
        'Equipment Tag No': f"EQ-{random.randint(10000,99999)}-{random.choice('ABCD')}",
        'Equipment Description': random.choice(['Centrifugal Pump','Heat Exchanger',
            'Control Valve','Pressure Vessel','Junction Box','Compressor',
            'Air Cooler','Separator','Motor','Transformer']),
        'Work Area Ownership': random.choice(OWNERSHIP),
        'System / Subsystem Ownership': random.choice(OWNERSHIP),
        'Work Description': fake.sentence(nb_words=20),
        'Tools and Equipments': random.choice(['Hand tools, Multimeter',
            'Chain block, Lifting belt','Scaffolding, Safety harness',
            'Welding machine, Grinder','Hydraulic torque wrench']),
        'Name of Permit Applicant': fake.name(),
        'Applicant Company': co,
        'Applicant Contact Number': str(random.randint(30000000,39999999)),
        'Applicant DEPARTMENT': dep,
        'Date Requested': fmt_dt(rd),
        'Estimated Work Start Date': fmt_dt(sd),
        'Late Submission': maybe('Yes', 0.15),
        'Valid From Date': fmt_dt(vf),
        'Valid To Date': fmt_dt(vt),
        'Name of PTW Coordinator': fake.name(),
        'Commented / rejected If any specify the Comments': maybe(fake.sentence(nb_words=15), 0.5),
        'Reviewed Date and Time': fmt_dt(rev),
        'Name of Concurred Party 1': maybe(fake.name(), 0.8),
        'Concurred Party 1 Department': maybe(random.choice(DEPARTMENTS), 0.8),
        'Name of Concurred Party 2': maybe(fake.name(), 0.5),
        'Concurred Party 2 Department': maybe(random.choice(DEPARTMENTS), 0.5),
        'Name of Concurred Party 3': maybe(fake.name(), 0.2),
        'Concurred Party 3 Department': maybe(random.choice(DEPARTMENTS), 0.2),
        'Concurred Date and Time': fmt_dt(con),
        'Name of HOS': maybe(fake.name(), 0.7),
        'Approved Date and Time': fmt_dt(apr),
        'Name of Area Authority (latest AA per revalidation)': fake.name(),
        'Authorised Date and Time': fmt_dt(apr + timedelta(hours=1)),
        'Name of Permit Issuer (latest issuer per revalidation)': maybe(fake.name(), 0.8),
        'Issued Date and Time': fmt_dt(iss),
        'Name of Permit Receiver (latest receiver per revalidation)': maybe(fake.name(), 0.75),
        'Received Date and Time': fmt_dt(rec),
        'Permit Closed by (name in section 13)': maybe(fake.name(), 0.5),
        'Closed Date and Time': fmt_dt(clo) if clo else None,
        'Remarks/Comments': maybe(fake.sentence(nb_words=10), 0.4),
        'Day /Night Shift\nPERMIT': random.choice(['Day','Night']),
        'Rescue Plan Number \n(if abvailable )': maybe(f"RP-{random.randint(100,999)}", 0.4),
        'TYPES OF Rescue Plan': random.choice(['WAH Rescue Plan','Confined Space Rescue','Fire Rescue','']),
        '1': maybe('X',0.3), '2': maybe('X',0.2), '3': maybe('X',0.15),
        '4': maybe('X',0.1), '5': maybe('X',0.05),
        'Start Date': vf,
        'End Date': vt,
        'status': random.choice(STATUSES_COL),
        'ACTUAL AREA': random.choice(ACTUAL_AREAS),
        'ACTUAL COMPANY': co,
        'MONTH': rd.strftime('%b-%Y'),
        'YEAR': rd.year,
        'DATE REQUESTED': rd.strftime('%d-%b-%Y'),
        'REVIEWED DATE ': rev.strftime('%d-%b-%Y'),
        'PERMIT RECEIVER \nDATE RECEIVED': rec.strftime('%d-%b-%Y') if random.random() < 0.75 else '',
    })

df = pd.DataFrame(rows)
df.to_excel('fake_ptw_data.xlsx', index=False, sheet_name='E-PTW ACTIVE')
print(f"Generated {len(df)} rows × {len(df.columns)} columns → fake_ptw_data.xlsx")
