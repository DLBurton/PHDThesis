#!/usr/bin/env python
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime, time
from optparse import OptionParser
import array
import math as m
from array import array

print " Selecting tdr style"
r.gROOT.ProcessLine(".L tdrstyle.C")
r.setstyle()
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
r.gStyle.SetPaintTextFormat("5.2f")

Run_Type = ["PtDistributions","HTDistributions"][1]

input_file = "./Muon_MC.root"
prefix = "OneMuon_"
if Run_Type == "HTDistributions" : bins = ["275_325","325_375","375_475","475_575","575_675","675_775","775_875","875"] 
else : bins = ["Template_375"] 
file = r.TFile.Open("%s"%input_file)
DirKeys = file.GetListOfKeys()

c1= r.TCanvas("Yields", "Yields",0,0,900,600)
c1.cd()

def make_histogram(path,numerator,denominator,colour=1,type=''):

    plot_dem = file.Get(path+"/"+denominator)
    plot_num = file.Get(path+"/"+numerator)

    
    plot = plot_num.Clone()
    plot_dem_clone = plot_dem.Clone()

    if type == "Pt": 
        axis_rebin = array('d',[25.,50.,75.,100.,125.,150.,175.,200.,250.,300.,350.,400.,450.,500.,700.,1000.,])

        plot_1 = plot.Rebin(len(axis_rebin)-1,"plot",axis_rebin)
        plot_2 = plot_dem_clone.Rebin(len(axis_rebin)-1,"plot",axis_rebin)
        plot_1.Divide(plot_2)
        plot_1.SetFillColor(colour)
        plot_1.SetLineColor(colour)
        return plot_1

    plot.Divide(plot_dem_clone)
    plot.SetFillColor(colour)
    plot.SetLineColor(colour)
    return plot
       
def make_ptdist_plot(htbin,flavour,xrange,yrange,plot_loose,plot_medium,plot_tight,leg_coords):
 
    c1.cd()
    c1.SetLogy(1)
    leg = Legend_Maker(leg_coords)
    leg.AddEntry(plot_loose,"Loose","L")
    leg.AddEntry(plot_medium,"Medium","L")
    leg.AddEntry(plot_tight,"Tight","L")
    
    plot_loose.GetXaxis().SetRangeUser(xrange[0],xrange[1])
    plot_loose.GetXaxis().SetTitle("Jet p_{T} (GeV)")
    plot_loose.GetXaxis().SetTitleOffset(1.3)

    plot_loose.GetYaxis().SetRangeUser(yrange[0],yrange[1])
    plot_loose.GetYaxis().SetTitle("Tagging Efficiency")
    plot_loose.GetYaxis().SetTitleOffset(1.1)
    plot_loose.Draw("P")
    plot_medium.Draw("PSAME")
    plot_tight.Draw("PSAME")
    leg.Draw("SAME")
    c1.SaveAs("%s_PtDistribution_Htbin_%s.pdf"%(flavour,htbin))

def Legend_Maker(coords): 
      leg = r.TLegend(coords[0],coords[1],coords[2],coords[3]) 
      leg.SetTextSize(0.04)
      leg.SetShadowColor(0)
      leg.SetBorderSize(0)
      leg.SetFillColor(0)
      leg.SetLineColor(0)
      return leg


Efficiencies_dict = {"Corrected":{},"Uncorrected":{}}

dict_entries = ('Btag_Efficiency','Mistag_Efficiency','Ctag_Efficiency','Btag_Error','Mistag_Error','Ctag_Error')

for key in Efficiencies_dict : 
   Efficiencies_dict[key] = dict.fromkeys(bins)
   for a in bins : Efficiencies_dict[key][a] = dict.fromkeys(dict_entries,0)

def pull_efficiencies(dir,denominator,numerator,htbin,corr = '',type=''):

    corr_dict = {"y":"Corrected","n":"Uncorrected"}
    type_dict = {"b":["Btag_Efficiency","Btag_Error"],"c":["Ctag_Efficiency","Ctag_Error"],"light":["Mistag_Efficiency","Mistag_Error"]}

    err_num = r.Double(0.0)     
    err_denom = r.Double(0.0) 
    
    plot_denom = file.Get(dir+"/"+denominator)
    plot_num = file.Get(dir+"/"+numerator)

    plot_num.IntegralAndError(1,10000,err_num)
    plot_denom.IntegralAndError(1,10000,err_denom)
     
    try : efficiency = plot_num.Integral()/plot_denom.Integral()
    except ZeroDivisionError : efficiency = 0

    

    try: denom_error = err_denom/plot_denom.Integral()
    except ZeroDivisionError: denom_error = 0
    try: numerator_error = err_num/plot_denom.Integral()
    except ZeroDivisionError: numerator_error = 0

    try : total_error = efficiency*m.sqrt(pow(denom_error,2)+pow(numerator_error,2))
    except ZeroDivisionError: total_error = 0

    Efficiencies_dict[corr_dict[corr]][htbin][type_dict[type][0]] = efficiency 
    Efficiencies_dict[corr_dict[corr]][htbin][type_dict[type][1]] = total_error

def make_htdist_plot(leg_coords,yrange,type=''):

    type_dict = {"b":["Btag_Efficiency","Btag_Error"],"c":["Ctag_Efficiency","Ctag_Error"],"light":["Mistag_Efficiency","Mistag_Error"]}

    data_nocorr = r.TH1F("","",8,array('d',[275,325,375,475,575,675,775,875,975]))
    data_corr = r.TH1F("","",8,array('d',[275,325,375,475,575,675,775,875,975]))
    correctiontype= "SF_{%s} Corrected"%type
    leg = Legend_Maker(leg_coords)
    leg.AddEntry(data_nocorr,"Uncorrected","L")
    leg.AddEntry(data_corr,correctiontype,"L")

    data_corr.SetLineColor(1)
    data_corr.SetFillColor(1)
    data_nocorr.SetLineColor(2)
    data_nocorr.SetFillColor(2)

    for i,entry in enumerate(bins):

        data_corr.SetBinContent(i+1,Efficiencies_dict["Corrected"][entry][type_dict[type][0]])
        data_nocorr.SetBinContent(i+1,Efficiencies_dict["Uncorrected"][entry][type_dict[type][0]])
        data_corr.SetBinError(i+1,Efficiencies_dict["Corrected"][entry][type_dict[type][1]])
        data_nocorr.SetBinError(i+1,Efficiencies_dict["Uncorrected"][entry][type_dict[type][1]])

    data_nocorr.GetYaxis().SetRangeUser(yrange[0],yrange[1])
    data_nocorr.GetYaxis().SetTitle("Tagging Efficiency")
    data_nocorr.GetYaxis().SetTitleOffset(1.25)
    data_nocorr.GetXaxis().SetTitle("H_{T} (GeV)")
    data_nocorr.GetXaxis().SetTitleSize(0.04)
    data_nocorr.GetXaxis().SetTitleOffset(1.25)
    data_nocorr.GetYaxis().SetLabelSize(0.04)
    data_nocorr.GetXaxis().SetLabelSize(0.04)


    data_nocorr.Draw("P")
    data_corr.Draw("SAME")
    leg.Draw("SAME")
    c1.SetLogy(0)
    c1.SaveAs("%s_jet_PtDistribution_Htbin.pdf"%(type))


for htbin in bins : 
  for entry in DirKeys:
    subdirect = file.FindObjectAny(entry.GetName())
    dir = prefix+htbin
    subdirect.GetName()
    if dir == subdirect.GetName():
      if Run_Type == "PtDistributions":
        
        loose = make_histogram(dir,"Btagged_GenJetPt_nBgen_PtDist_Loose_all","GenJetPt_nBgen_PtDist_all",colour=1,type="Pt") 
        medium = make_histogram(dir,"Btagged_GenJetPt_nBgen_PtDist_Medium_all","GenJetPt_nBgen_PtDist_all",colour=2,type="Pt") 
        tight = make_histogram(dir,"Btagged_GenJetPt_nBgen_PtDist_Tight_all","GenJetPt_nBgen_PtDist_all",colour=4,type="Pt") 
        make_ptdist_plot(htbin,"bjet",[25.,600.],[0.1,1.3],loose,medium,tight,[0.12,0.14,0.4,0.34])

        loose = make_histogram(dir,"Btagged_GenJetPt_c_nBgen_PtDist_Loose_all","GenJetPt_c_nBgen_PtDist_all",colour=1,type="Pt") 
        medium = make_histogram(dir,"Btagged_GenJetPt_c_nBgen_PtDist_Medium_all","GenJetPt_c_nBgen_PtDist_all",colour=2,type="Pt") 
        tight = make_histogram(dir,"Btagged_GenJetPt_c_nBgen_PtDist_Tight_all","GenJetPt_c_nBgen_PtDist_all",colour=4,type="Pt") 
        make_ptdist_plot(htbin,"cjet",[25.,600.],[0.005,1.3],loose,medium,tight,[0.12,0.14,0.35,0.34])

        loose = make_histogram(dir,"Btagged_GenJetPt_noB_nBgen_PtDist_Loose_all","GenJetPt_noB_nBgen_PtDist_all",colour=1,type="Pt") 
        medium = make_histogram(dir,"Btagged_GenJetPt_noB_nBgen_PtDist_Medium_all","GenJetPt_noB_nBgen_PtDist_all",colour=2,type="Pt") 
        tight = make_histogram(dir,"Btagged_GenJetPt_noB_nBgen_PtDist_Tight_all","GenJetPt_noB_nBgen_PtDist_all",colour=4,type="Pt") 
        make_ptdist_plot(htbin,"lighjet",[25.,600.],[0.0005,1.3],loose,medium,tight,[0.72,0.65,0.88,0.88])

      if Run_Type == "HTDistributions": 

        pull_efficiencies(dir,"GenJetPt_nBgen_all", "Btagged_GenJetPt_nBgen_SFb_Medium_all",htbin,corr="y",type="b")
        pull_efficiencies(dir,"GenJetPt_nBgen_all", "Btagged_GenJetPt_nBgen_Medium_all",htbin,corr="n",type="b")

        pull_efficiencies(dir,"GenJetPt_c_nBgen_all", "Btagged_GenJetPt_c_nBgen_SFlight_Medium_all",htbin,corr="y",type="c")
        pull_efficiencies(dir,"GenJetPt_c_nBgen_all", "Btagged_GenJetPt_c_nBgen_Medium_all",htbin,corr="n",type="c")

        pull_efficiencies(dir,"GenJetPt_noB_nBgen_all", "Btagged_GenJetPt_noB_nBgen_SFlight_Medium_all",htbin,corr="y",type="light")
        pull_efficiencies(dir,"GenJetPt_noB_nBgen_all", "Btagged_GenJetPt_noB_nBgen_Medium_all",htbin,corr="n",type="light")

make_htdist_plot([0.65,0.65,0.80,0.88],[0.5,0.9],type="b")
make_htdist_plot([0.65,0.65,0.80,0.88],[0.1,0.3],type="c")
make_htdist_plot([0.65,0.65,0.80,0.88],[0.005,0.05],type="light")

   
