import requests
import re


def roosterical(som_ical_url):
    response = requests.get(som_ical_url)
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

    ical_content = "\n".join(modified_ical)

    return ical_content


roosterical(som_ical_url)
