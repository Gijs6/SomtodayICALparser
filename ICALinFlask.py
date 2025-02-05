from flask import Flask, Response
import requests
import re

app = Flask(__name__)

@app.route("/rooster")
def roosterical():
    response = requests.get(SOM_ICAL_URL)
    response.raise_for_status()

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
                lokaal = isEenLes.group(1)
                lesgroep = isEenLes.group(2)
                docent = isEenLes.group(3)

                vakafko = ""

                for afkorting in vakkenlijst.keys():
                    if afkorting in lesgroep:
                        vakafko = vakkenlijst[afkorting]
                if not vakafko:
                    vakafko = lesgroep

                nieuwe_lijn = "SUMMARY:" + vakafko + " (" + lokaal + " - " + docent + ")"
            else:
                nieuwe_lijn = line

        else:
            nieuwe_lijn = line
        modified_ical.append(nieuwe_lijn)

    new_ical_content = "\n".join(modified_ical)

    return Response(
        new_ical_content,
        mimetype="text/calendar",
        headers={"Content-Disposition": "attachment; filename=modified.ical"}
    )


if __name__ == '__main__':
    app.run(debug=True)
