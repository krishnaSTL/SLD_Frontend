import requests
from tkinter import messagebox
import json
import sys


def getDropDownData():
        try:
            url = "https://nssbsurvey.sterliteapps.com/api/v1/data/s23_2639?filter=${the_geom} is not null&bad=none"
            headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Basic YXNoaXNoLmdpamFtQHN0bC50ZWNoOlN0ZXJsaXRlQDEyMzQ1'
            }

            response = requests.request("GET", url, headers=headers)
            json_data = json.loads(response.text)
            results = {}
            for data in json_data:
                pkg = str(data['Case Survey'])
                if pkg == "":
                    pkg = 'NULL'
                distrct = str(data['CMP_Name'])
                if distrct == "":
                    distrct = 'NULL'
                mandal = str(data['_alert'])
                if mandal == "":
                    mandal = 'NULL'
                spn_nm = str(data['Span_Name'])
                if spn_nm == "":
                    spn_nm = 'NULL'
                if pkg not in results.keys():
                    results[pkg] = {}
                if distrct not in results[pkg].keys():
                    results[pkg][distrct] = {}
                if mandal not in results[pkg][distrct].keys():
                    results[pkg][distrct][mandal] = {}
                if spn_nm not in results[pkg][distrct][mandal].keys():
                    results[pkg][distrct][mandal][spn_nm] = [distrct, mandal]
            return results
        except:
            messagebox.showinfo('STL', f'Error Connecting To PostGIS: {str(sys.exc_info())}')

results = getDropDownData()

def selPkg(self, event):
        distrcts = list(self.results[self.cmbPkg.get()].keys())
        distrcts.sort()
        self.cmbDistrct.configure(values = distrcts, state="normal")
        self.cmbDistrct.set("Select District")
        self.cmbMandal.configure(values = [], state="disabled")
        self.cmbMandal.set("Select Mandal")
        self.cmbSpan.configure(values = [], state="disabled")
        self.cmbSpan.set("Select Span")
        
        self.btnExport.configure(state="disabled")


# print("the results are ", results)
######################################################################
# <script>
#                 document.addEventListener("DOMContentLoaded", function () {
#                     fetch('/dropdown_data')
#                         .then(response => response.json())
#                         .then(data => {
#                             const packageSelect = document.getElementById('packageSelect');
#                             const districtSelect = document.getElementById('districtSelect');
#                             const mandalSelect = document.getElementById('mandalSelect');
#                             const spanSelect = document.getElementById('spanSelect');
        
#                             for (const pkg in data) {
#                                 const option = document.createElement('option');
#                                 option.textContent = pkg;
#                                 packageSelect.appendChild(option);
#                             }
        
#                             packageSelect.addEventListener('change', function () {
#                                 const selectedPackage = packageSelect.value;
#                                 districtSelect.innerHTML = '<option selected>Choose District...</option>';
#                                 mandalSelect.innerHTML = '<option selected>Choose Mandal...</option>';
#                                 spanSelect.innerHTML = '<option selected>Choose Span...</option>';
        
#                                 if (selectedPackage !== 'Choose Package...') {
#                                     for (const district in data[selectedPackage]) {
#                                         const option = document.createElement('option');
#                                         option.textContent = district;
#                                         districtSelect.appendChild(option);
#                                     }
#                                 }
#                             });
        
#                             districtSelect.addEventListener('change', function () {
#                                 const selectedPackage = packageSelect.value;
#                                 const selectedDistrict = districtSelect.value;
#                                 mandalSelect.innerHTML = '<option selected>Choose Mandal...</option>';
#                                 spanSelect.innerHTML = '<option selected>Choose Span...</option>';
        
#                                 if (selectedPackage !== 'Choose Package...' && selectedDistrict !== 'Choose District...') {
#                                     for (const mandal in data[selectedPackage][selectedDistrict]) {
#                                         const option = document.createElement('option');
#                                         option.textContent = mandal;
#                                         mandalSelect.appendChild(option);
#                                     }
#                                 }
#                             });
        
#                             mandalSelect.addEventListener('change', function () {
#                                 const selectedPackage = packageSelect.value;
#                                 const selectedDistrict = districtSelect.value;
#                                 const selectedMandal = mandalSelect.value;
#                                 spanSelect.innerHTML = '<option selected>Choose Span...</option>';
        
#                                 if (selectedPackage !== 'Choose Package...' && selectedDistrict !== 'Choose District...'
#                                     && selectedMandal !== 'Choose Mandal...') {
#                                     for (const span in data[selectedPackage][selectedDistrict][selectedMandal]) {
#                                         const option = document.createElement('option');
#                                         option.textContent = span;
#                                         spanSelect.appendChild(option);
#                                     }
#                                 }
#                             });
#                         });
#                 });
#             </script>