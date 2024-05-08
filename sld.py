    
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime
from PIL import Image
import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2
import folium
from selenium import webdriver
import time
import tkinter
from tkinter import messagebox
import sys
from folium import plugins
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())

# from geopy.distance import geodesic
import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")






def createSLD(pkg, distrct, mandal, spn_nm, frmGP, toGP):
    ###########<Paper size>##########
    paper_size_mm = {'A0': [841, 1189], 'A1_': [694, 941], 'A1': [594, 841], 'A2': [420, 594], 'A3': [297, 420], 'A4': [210, 297], 'A5': [148, 210], 'A6': [105, 148], 'A7': [74, 105], 'A8': [52, 74], 'A9': [37, 52], 'A10': [26, 37]}
    paper_size_inch = {'A0': [33.1, 46.8], 'A1': [23.4, 33.1], 'A2': [16.5, 23.4], 'A3': [11.7, 16.5], 'A4': [8.3, 11.7], 'A5': [5.8, 8.3], 'A6': [4.1, 5.8], 'A7': [2.9, 4.1], 'A8': [2, 2.9], 'A9': [1.5, 2], 'A10': [1, 1.5]}
    # paper = paper_size_inch['A0']
    paper = paper_size_mm['A1_']

    _h = (paper[1] + ((paper[1]*9)/100))
    _w = (paper[0] + ((paper[1]*10)/100))

    dpi=72
    mm_2_inch = 25.4

    w = (_h*dpi)/mm_2_inch
    h = (_w*dpi)/mm_2_inch

    size = (_h/mm_2_inch, _w/mm_2_inch)

    # frm_dt = '2021-04-11'
    # to_dt = '2024-05-03'

    ##########Add Scope line
    url = "https://nssbsurvey.sterliteapps.com/api/v1/data/s23_2639?filter=${span_name} = '" + spn_nm + "' and ${CMP_Name} = '" + distrct + "' and ${_alert} = '" + mandal + "' and ${_case_survey} = '" + pkg + "' and ${the_geom} is not null&bad=none"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Basic YXNoaXNoLmdpamFtQHN0bC50ZWNoOlN0ZXJsaXRlQDEyMzQ1'
    }

    response = requests.request("GET", url, headers=headers)

    ex_scpe = 0
    ex_comp = 0
    # mandal = 'Jaipur'
    # distrct = 'Kishangarh'
    # frmGP = 'Jaipur'
    # toGP = 'Kishangarh'


    json_data = json.loads(response.text)
    st_cords = json_data[0]['the_geom']['coordinates'][0]
    st_cords = (st_cords[1], st_cords[0])
    end_cords = json_data[0]['the_geom']['coordinates'][-1]
    end_cords = (end_cords[1], end_cords[0])
    m = folium.Map(location=st_cords, zoom_start=10)
    

    
    
       






    ln_exect_comp = folium.FeatureGroup(name='Execution Completed')
    ln_exect_scope = folium.FeatureGroup(name='Scope')

    cords = []
    for cord in json_data[0]['the_geom']['coordinates']:
        cords.append((cord[1], cord[0]))
    line_segment = folium.PolyLine(cords, color='Green', weight=0.2, opacity=0.3).add_to(m)

    for data in json_data:
        cords = []
        for cord in data['the_geom']['coordinates']:
            cords.append((cord[1], cord[0]))
        if data['Survey_Length'] != "":
            try:
                len_ = float(data['Survey_Length'])
                ex_scpe += len_
            except:
                pass
        folium.PolyLine(locations=cords, color='Red', weight=3.5, opacity=1).add_to(ln_exect_scope)


    ##########Add Execution Completed line
    url = "https://nssbsurvey.sterliteapps.com/api/v1/data/s23_67?filter=${span_name} = '" + spn_nm + "' and ${CMP_Name} = '" + distrct + "' and ${_alert} = '" + mandal + "' and ${_case_survey} = '" + pkg + "' and ${q1} = 'true' and ${the_geom} is not null&bad=none"

    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    
    
    for data in json_data:
        cords = []
        for cord in data['the_geom']['coordinates']:
            cords.append((cord[1], cord[0]))
            
        
        if data['Surve_Length'] != "":
            try:
                len_ = float(data['Surve_Length'])
                ex_comp += len_
            except:
                pass
        folium.PolyLine(locations=cords, color='Green', weight=3.5, opacity=1).add_to(ln_exect_comp)


    ln_exect_scope.add_to(m)
    ln_exect_comp.add_to(m)


    # Add Layer Control Panel to manage layers
    folium.LayerControl().add_to(m)


    m.fit_bounds(line_segment.get_bounds(), padding=(6, 6))



    # Save the map to an HTML file
    m.save(r'map.html')


    # Use Selenium to take a screenshot
    driver = webdriver.Edge()  # Make sure ChromeDriver is in your PATH
    driver.get(os.getcwd() + r'\\map.html')
    # Increased waiting time for rendering
    import time
    time.sleep(1)
    # Execute JavaScript to simulate a few zoom-in clicks
    # for _ in range(1):  # Adjust the number of zoom-in clicks as needed
        # driver.execute_script(f"document.querySelector('div.leaflet-control-zoom a.leaflet-control-zoom-in').click();")

    driver.save_screenshot(r'map.png')

    # Close the browser
    driver.quit()

    m = folium.Map(location=st_cords, zoom_start=10)
    ln_exect_scope.add_to(m)
    ln_exect_comp.add_to(m)
    # Add a satellite imagery tile layer
    satellite_tile_layer = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=True,
        control=True
    )
    satellite_tile_layer.add_to(m)

    #### Add OpenStreetMap (OSM) tiles
    folium.TileLayer(tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attr='OSM', name='OpenStreetMap', overlay=True, control=True).add_to(m)

    #### Overwrite the map to an HTML file
    # Add Layer Control Panel to manage layers
    attr = {"fill": "black", "font-weight": "bold", "font-size": "12"}
    len_ = 0
    for data in json_data:
        cords = []
        for cord in data['the_geom']['coordinates']:
            cords.append((cord[1], cord[0]))
            
        if data['Surve_Length'] != "":
            try:
                len_ = float(data['Surve_Length'])
            except:
                pass

        pl = folium.PolyLine(cords, color='Green', weight=0.1, opacity=0.2)
        #### dist_km = geodesic(bangalore_coords, hyderabad_coords).kilometers
        textPath = plugins.PolyLineTextPath(
            pl, str(round(len_, 2)) + " Km", offset=-10 # Place label at the midpoint
            , attributes=attr
        )
        m.add_child(pl)
        m.add_child(textPath)
    # Add Layer Control Panel to manage layers
    folium.LayerControl().add_to(m)

    m.fit_bounds(line_segment.get_bounds(), padding=(12, 12))
    m.save(r'map.html')

    pdf_canvas = canvas.Canvas('sld_.pdf', pagesize=letter)
    fig = plt.figure(figsize=size, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.axis('off')

    px, py = 0, 0
    ####Left Border Line
    plt.vlines(px, 0, h, linestyles = 'solid', colors = '#000000', lw = 1)

    ####Top Border Line
    plt.hlines(h, 0, w, linestyles = 'solid', colors = '#000000', lw = 1)

    ####Right Border Line
    plt.vlines(w, 0, h, linestyles = 'solid', colors = '#000000', lw = 1)

    ####Bottom Border Line
    plt.hlines(py, 0, w, linestyles = 'solid', colors = '#000000', lw = 1)

    ######Writing SLD lines

    ##### Add Title here
    plt.text((w / 2) - (805/2),  h + 26, 'Simple Line Diagram', fontsize = 60, color = 'Black', weight = 'bold')

    #### Create Legend Box
    d_w = w
    x_min = (d_w*2) / 100
    x_max = (d_w*2) / 100
    l_x = 0
    l_y = (h - (h*6.2) / 100)
    t_mrg = ((((h*6.2) / 100)*30) / 100)
    l_mrg = (((d_w*11) / 100)*7) / 100
    txt_y = h-t_mrg

    plt.text(l_x+l_mrg, txt_y, 'Originator', fontsize = 24, color = 'Black', weight = 'bold')
    ####Add Image
    path = r"images\originator.png"
    img = mpimg.imread(path)
    imgBox = OffsetImage(img, zoom=1.25)
    annoBox = AnnotationBbox(imgBox,(l_x + l_mrg +120, (txt_y-t_mrg)-5), frameon = False)
    ax.add_artist(annoBox)
    l_x = l_x + ((d_w*10) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)

    ####Add legend
    plt.text(l_x+l_mrg, txt_y, 'Legend', fontsize = 24, color = 'Black', weight = 'bold')

    ###Add display Line : Scope
    plt.hlines((txt_y - t_mrg)+8, l_x+l_mrg+30, l_x+l_mrg +90, linestyles = 'solid', colors = 'Red', lw = 7)
    plt.text(l_x+l_mrg+110, txt_y- t_mrg, f'Scope  ( {round(ex_scpe,2)} Km )', fontsize = 27, color = 'Black')

    ###Add display Line : Scope
    plt.hlines((txt_y - t_mrg) - 32, l_x+l_mrg+30, l_x +l_mrg+90, linestyles = 'solid', colors = 'Green', lw = 7)
    plt.text(l_x+l_mrg+110, (txt_y- t_mrg)-40, f'Execution Completed  ( {round(ex_comp,2)} Km )', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*23.5) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)

    ####Add Info
    plt.text(l_x+l_mrg, txt_y, 'District', fontsize = 24, color = 'Black', weight = 'bold')
    plt.text(l_x+l_mrg + 30, (txt_y- t_mrg)-10, f'{distrct}', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*10) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)


    plt.text(l_x+l_mrg, txt_y, 'Mandal', fontsize = 24, color = 'Black', weight = 'bold')
    plt.text(l_x+l_mrg + 30, (txt_y- t_mrg)-10, f'{mandal}', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*10) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)


    plt.text(l_x+l_mrg, txt_y, 'Span Name', fontsize = 24, color = 'Black', weight = 'bold')
    plt.text(l_x+l_mrg + 30, (txt_y- t_mrg)-10, f'{spn_nm}', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*15) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)


    plt.text(l_x+l_mrg, txt_y, 'From GP', fontsize = 24, color = 'Black', weight = 'bold')
    plt.text(l_x+l_mrg + 30, (txt_y- t_mrg)-10, f'{frmGP}', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*10.5) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)


    plt.text(l_x+l_mrg, txt_y, 'To GP', fontsize = 24, color = 'Black', weight = 'bold')
    plt.text(l_x+l_mrg + 30, (txt_y- t_mrg)-10, f'{toGP}', fontsize = 27, color = 'Black')
    l_x = l_x + ((d_w*10.5) / 100)
    plt.vlines(l_x, h, l_y, linestyles = 'solid', colors = '#000000', lw = 1)


    ####Add Issue Date
    plt.text(l_x+l_mrg, txt_y, 'Issue Date', fontsize = 24, color = 'Black', weight = 'bold')
    #### get current date
    time = datetime.now()
    current_date = time.strftime("%d-%b-%y")
    plt.text(l_x+l_mrg +30, (txt_y - t_mrg)-10, str(current_date), fontsize = 32, color = 'Black')

    plt.hlines(l_y, 0, d_w, linestyles = 'solid', colors = '#000000', lw = 1)



    ##### Draw Scope Line
    x = x_min
    y = l_y - 250

    ## Scope Line
    plt.hlines(y, x, d_w - x_max, linestyles = 'solid', colors = 'Red', lw = 7)

    #### Add Marker / Point at Start & End
    plt.plot(x, y, marker="o", markersize=40, markeredgecolor="black", markerfacecolor="Green")
    plt.text(x, y-65,'Jaipur', fontsize = 32, color = 'Black', weight = 'bold')

    plt.plot(d_w - x_max, y, marker="o", markersize=40, markeredgecolor="black", markerfacecolor="Green")
    plt.text((d_w - x_max), y-65, 'Kishangarh', fontsize = 32, color = 'Black', weight = 'bold', ha = 'right')

    plt.text((d_w / 2) - 10, y + 30, f'{round(ex_scpe,2)} Km', fontsize = 50, color = 'Black', weight = 'bold')


    y = l_y - 500
    ## Scope Line
    ### Calculate Line Width
    wdt = ((d_w - x_max) * (ex_comp / ex_scpe)*100)/100
    plt.hlines(y, x, wdt, linestyles = 'solid', colors = 'Green', lw = 7)
    plt.plot(x, y, marker="o", markersize=40, markeredgecolor="black", markerfacecolor="Green")
    plt.plot(wdt, y, marker="o", markersize=40, markeredgecolor="black", markerfacecolor="Green")

    plt.text((wdt / 2) - 10, y + 30, f'{round(ex_comp,2)} Km', fontsize = 50, color = 'Black', weight = 'bold')


    y = l_y - 700

    plt.text(10, y, 'Double Click on Map to view Map in Web', fontsize = 30, color = 'Black', weight = 'bold')


    #### Add Map Image to PDF Drawing
    path = r"map.png"
    img = Image.open(path)
    width, height = img.size
    left = 90
    top = 170
    img = img.crop((left, top, width - 70, height - 130))
    imgBox = OffsetImage(img, zoom=2.3)
    annoBox = AnnotationBbox(imgBox,((d_w / 2), y-700), frameon = False)
    ax.add_artist(annoBox)


    ### Crop Image & Save as PDF
    fig.savefig(r"tmp.png", format="png", transparent=False, bbox_inches='tight', pad_inches=0)
    plt.close()
    im = Image.open(r"tmp.png")
    #### Setting the points for cropped image
    width, height = im.size
    left = ((width*4)/100)
    top = 20
    right = width - ((width*4)/100)
    bottom = height - ((height*4)/100)
    #### Cropped image of above dimension
    im1 = im.crop((left, top, right, bottom))
    # im1 = im1.save(r"{0}_{1}.pdf".format(frm_dt, cnt_1))
    # Get the size of the image
    img_width, img_height = im1.size

    # Add a new page to the PDF
    pdf_canvas.setPageSize((img_width, img_height))
    pdf_canvas.showPage()

    pdf_canvas.linkURL(r'map.html', (0, y-65, d_w, 0), relative=1)
    # Draw the image on the PDF
    pdf_canvas.drawInlineImage(im1, 0, 0, width=img_width, height=img_height)
    pdf_canvas.save()
            
            
        
    with open(os.getcwd() + r'\\sld_.pdf', 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)

        if total_pages > 1:
            with open(r'sld.pdf', 'wb') as output_file:
                pdf_writer = PyPDF2.PdfWriter()

                # Add pages to the new PDF, excluding the first page
                for page_number in range(1, total_pages):
                    pdf_writer.add_page(pdf_reader.pages[page_number])

                pdf_writer.write(output_file)

    os.remove(r"sld_.pdf")
    os.remove(r"tmp.png")
    # os.remove(r"map.html")
    os.remove(r"map.png")
    
    messagebox.showinfo('STL', 'SLD Generated Successfully!')
    os.startfile("sld.pdf")





class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.results = self.getDropDownData()
    
        # configure window
        self.title("STL Auto SLD")
        self.geometry(f"{380}x{200}")
        self.minsize(380, 200)
        self.maxsize(380, 200)
        
        # label_1 = customtkinter.CTkLabel(self, text="State", justify=customtkinter.LEFT)
        # label_1.pack(row=0, column=0, padx=20, pady=(10, 10))
        
        pkg_list = list(self.results.keys())
        pkg_list.sort()
        self.cmbPkg = customtkinter.CTkOptionMenu(self, dynamic_resizing=True, anchor='w', values=pkg_list, command=self.selPkg)
        self.cmbPkg.grid(row=0, column=0,padx=10, pady=(10, 10))
        self.cmbPkg.set("Select Package")
        
        

        self.cmbDistrct = customtkinter.CTkOptionMenu(self, dynamic_resizing=True, anchor='w', state="disabled", command=self.selDistrct)
        self.cmbDistrct.grid(row=1, column=0,padx=10, pady=(10, 10))
        self.cmbDistrct.set("Select District")
        

        self.cmbMandal = customtkinter.CTkOptionMenu(self, dynamic_resizing=True, anchor='w', state="disabled", command=self.selMandal)
        self.cmbMandal.grid(row=2, column=0,padx=10, pady=(10, 10))
        self.cmbMandal.set("Select Mandal")
        
        
        
        self.cmbSpan = customtkinter.CTkOptionMenu(self, dynamic_resizing=True, anchor='w', state="disabled", command=self.selSpan)
        self.cmbSpan.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.cmbSpan.set("Select Span")
        
        
        self.btnExport = customtkinter.CTkButton(self, text="Export", state="disabled", command=self.export)
        self.btnExport.grid(row=3, column=1, padx=10, pady=(10, 10))
        
        
    def getDropDownData(self):
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
        
    def selDistrct(self, event):
        mandals = list(self.results[self.cmbPkg.get()][self.cmbDistrct.get()].keys())
        mandals.sort()
        self.cmbMandal.configure(values = mandals, state="normal")
        self.cmbMandal.set("Select Mandal")
        self.cmbSpan.configure(values = [], state="disabled")
        self.cmbSpan.set("Select Span")
        self.btnExport.configure(state="disabled")
        
    def selMandal(self, event):
        spans = list(self.results[self.cmbPkg.get()][self.cmbDistrct.get()][self.cmbMandal.get()].keys())
        spans.sort()
        self.cmbSpan.configure(values = spans, state="normal")
        self.cmbSpan.set("Select Span")
        self.btnExport.configure(state="disabled")
        
    def selSpan(self, event):
        self.btnExport.configure(state="normal")
        
    def export(self):
        pkg = self.cmbPkg.get()
        distrct = self.cmbDistrct.get()
        mandal = self.cmbMandal.get()
        spn_nm = self.cmbSpan.get()
        frmGP = self.results[self.cmbPkg.get()][self.cmbDistrct.get()][self.cmbMandal.get()][self.cmbSpan.get()][0]
        toGP = self.results[self.cmbPkg.get()][self.cmbDistrct.get()][self.cmbMandal.get()][self.cmbSpan.get()][1]
        createSLD(pkg, distrct, mandal, spn_nm, frmGP, toGP)
    def close(self):
        self.destroy()
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
            


