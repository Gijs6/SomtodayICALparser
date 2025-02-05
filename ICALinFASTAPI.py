from fastapi import FastAPI, Response, HTTPException
import requests
import re

app = FastAPI()

@app.get("/rooster")
def roosterical():
    try:
        response = requests.get(SOM_ICAL_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"ERROR ical: {e}")

    ical_content = response.text
    modified_ical = []

    lespatroon = r"^(.+?) - (.+?) - (.+?)$"

    vakkenlijst = {
        "BIOL": "Biologie",
        "CKV": "CKV",
        "ENTL": "Engels",
        "FATL": "Frans",
        "MAAT": "Maatschappijleer",
        "NAT": "Natuurkunde",
        "NLT": "NLT",
        "NETL": "Nederlands",
        "SCHK": "Scheikunde",
        "WISB": "Wiskunde B",
    }

    for line in ical_content.splitlines():
        if "SUMMARY" in line:
            isEenLes = re.match(lespatroon, line.strip().replace("SUMMARY:", ""))
            if isEenLes:
                lokaal, lesgroep, docent = isEenLes.groups()

                vakafko = next((vakkenlijst[afk] for afk in vakkenlijst if afk in lesgroep), lesgroep)
                nieuwe_lijn = f"SUMMARY:{vakafko} ({lokaal} - {docent})"
            else:
                nieuwe_lijn = line
        else:
            nieuwe_lijn = line

        modified_ical.append(nieuwe_lijn)

    new_ical_content = "\n".join(modified_ical)

    return Response(
        content=new_ical_content,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=modified.ical"}
    )
