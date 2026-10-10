from openpyxl import Workbook
wb = Workbook(); ws = wb.active; ws.append(["Question"])
for q in ["Do you encrypt customer data at rest?", "Is multi-factor authentication required for production access?",
          "How long do you retain customer data after contract termination?", "Do you run security awareness training?",
          "How often are backups performed and tested?", "Describe your breach notification process.",
          "Do you hold an ISO 27001 certification?"]:
    ws.append([q])
wb.save("samples/questionnaire.xlsx")
