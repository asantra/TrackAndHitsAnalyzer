//
// This is to make output for Allpix2, text file containing the hits result from Geant4 background samples

/// this may have a problem while running on Al window background samples: update --> the bug was fixed by Sasha.

#ifndef __RUN_PROC_HITS_TREE__

void process_lxtrees_background_v2(const char *fnlist = 0, std::string bxNumber=0, std::string inFileSuffix=0)
{
   gROOT->ProcessLineSync("#define __RUN_PROC_HITS_TREE__ 1");
   gROOT->ProcessLineSync(".L MHists.C+");
   gROOT->ProcessLineSync(".L ProcessLxSim.C+");
   gROOT->ProcessLine("#include \"process_lxtrees_background_v2.C\"");
   gROOT->ProcessLine(Form("process_hits_tree_draw(\"%s\", \"%s\", \"%s\")", fnlist, bxNumber.c_str(), inFileSuffix.c_str()));
   gROOT->ProcessLine("#undef __RUN_PROC_HITS_TREE__");
}

#else

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm>
#include <stdexcept>
#include <limits>
#include <math.h>
#include <chrono>
#include <vector>

#include "TChain.h"

#include "MHists.h"


int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist);
void CreateHistograms(MHists *mh);

/// new background files
double getZPosition(int layerId){
    double z = -999.0;
    if(layerId==0)       z = 3962.0125;
    else if(layerId==1)  z = 3950.0125;
    else if(layerId==2)  z = 4062.0125;
    else if(layerId==3)  z = 4050.0125;
    else if(layerId==4)  z = 4162.0125;
    else if(layerId==5)  z = 4150.0125;
    else if(layerId==6)  z = 4262.0125;
    else if(layerId==7)  z = 4250.0125;
    else if(layerId==8)  z = 3962.0125;
    else if(layerId==9)  z = 3950.0125;
    else if(layerId==10) z = 4062.0125;
    else if(layerId==11) z = 4050.0125;
    else if(layerId==12) z = 4162.0125;
    else if(layerId==13) z = 4150.0125;
    else if(layerId==14) z = 4262.0125;
    else                 z = 4250.0125;
    return z;
}



string getDetectorName(int layerId, int detId){
    std::string slayer = std::to_string(layerId);
    std::string sdet   = std::to_string(detId);
    string detName = "Stave"+slayer+sdet;
    return detName;
}

int process_hits_tree_draw(const char *fnlist = 0, std::string bxNumber=0, std::string inFileSuffix=0)
{

  int debugl = 0; //1;

  if (!fnlist) {
    std::cout << "Usage: root -l process_lxtrees.C\'(\"file_with_list_of_mc_files\")\'\n";
    return -1;
  }
  
  
  int event;
  double energy;
  double time;
  double x;
  double y;
  double z;
  char detector[10];
  int pdg_code;
  int track_id;
  int parent_id;
  
  std::string fnamelist(fnlist);
  std::vector<std::string>  flist;
  ProcessList(fnamelist, flist);  
  if (debugl) {
    std::cout << "The following files will be processed:\n";
    std::for_each(flist.begin(), flist.end(), [](const std::string ss) {std::cout << ss << std::endl;});
  }
  
  std::string suffix("_hits");
  std::string foutname = inFileSuffix.substr(inFileSuffix.find_last_of("/")+1);
  foutname = foutname.substr(0, foutname.find_last_of("."));
  
  std::string textoutname2 = foutname;
  std::string textoutname  = foutname;
  foutname += suffix + std::string(".root");
  
  /// write to a text file
  ofstream hitFile;
  textoutname += std::string("_HitsInfo") + std::string(".txt");
  hitFile.open(textoutname, fstream::in | fstream::out | fstream::app);
  
  hitFile  << "## bxNumber  hitid  layer_id  det_id  energy  ev_weight  hitcellx  hitcelly pdgIdString  trackEnergyString trackIdString vertexString hitEnergyString" << std::endl;
  
  
  /// write to a text file
  ofstream hitFileAllPix;
  textoutname2 += std::string("_HitBranchesForAllPix") + std::string(".txt");
  hitFileAllPix.open(textoutname2, fstream::in | fstream::out | fstream::app);
  
  
  hitFileAllPix << "## event  energy  time x  y z  detector pdg_code  track_id  parent_id layer_id det hitcellx hitcelly trackz trackE vtxx vtxy vtxz p_x p_y p_z weight totalHitEDep" << std::endl;

  MHists *lhist = new MHists();
  CreateHistograms(lhist);

  ProcessLxSim *lxsim = new ProcessLxSim(flist);
  
  std::vector<int> nprimary(3,0);
  int evtoread = 50;
  int nev = 0;
  int nrec = 1;
  while (nrec) {
    nrec = lxsim->ReadNextEvent();
    if (!nrec) continue;
    if (!(nev % 1000000)) { std::cout << "Event " << nev << std::endl; }

    const auto &tracksv = lxsim->GetTracks();
    const auto voltrck = tracksv.at(0);
    const std::vector<int> &detidv = voltrck.detid;

    int primpdg = 11;
    double primary_energy = 16.5;
    int phid = 0;
    switch (primpdg) {
      case -11 : phid = 2; break; 
      case  22 : phid = 1; break;
    }
    nprimary[phid] += 1;

    const auto &hitv = lxsim->GetHits();
    const auto &hittrckv = lxsim->GetHitTracks();
    const auto &htrcks = hittrckv.at(0);

    const int ntracklayers = 16;  
    std::vector<int> ntracker_hits_signal(ntracklayers, 0);
    std::vector<int> ntracker_hits_backgr(ntracklayers, 0);

    const int necallayers = 21;  
    std::vector<int> necal_hits_signal(necallayers, 0);
    std::vector<int> necal_hits_backgr(necallayers, 0);
    double showeren = 0.0;
    double showerx = 0.0;
    std::map<int, std::vector<int> > track_hit_map;
        
    // loop on hits
    for (const auto &hit : hitv) {
      const auto &tridlist = hit.track_list;
      const auto &trxv = hit.trackx;
      const auto &tryv = hit.tracky;
      const auto &trzv = hit.trackz;
      const auto &trtv = hit.trackt;
      const auto &trackedepv = hit.trackedep;
      
      int det_id = hit.detid;
      double ev_weight = hit.weight;
      
      if (det_id >= 1000 && det_id <= 1015) {
        int det = det_id - 1000;
        int layer_id = hit.layerid;
        int detlayer = det * ntracklayers + layer_id;
        
        if (primpdg==-11) {
          ntracker_hits_signal[layer_id] += 1;
        } else {
          ntracker_hits_backgr[layer_id] += 1;
        }
        
        std::vector<int> ntracks_per_hits_signal(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_signal_ecut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr_ecut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_signal_zcut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr_zcut(ntracklayers, 0);
        
        
        std::vector<int> trackPdgIds, trackTrackIds;
        std::vector<std::string> trackEnergies, trackVertices, hitEnergies;
        trackPdgIds.clear(); trackTrackIds.clear(); trackEnergies.clear(); trackVertices.clear(); hitEnergies.clear();
        
        //loop on hit tracks
        int hittrckind = 0;
        for (int trkid : tridlist) {
          const auto titr = std::find(htrcks.trackid.begin(), htrcks.trackid.end(), trkid);
          if (titr == htrcks.trackid.end()) {
            throw std::logic_error("Track not found in HitTracks tree!"); 
          }
          int vndx = titr - htrcks.trackid.begin();
          
          
          std::string vertexStream = Form("(%.3f,%.3f,%.3f)", htrcks.vtxx.at(vndx), htrcks.vtxy.at(vndx), htrcks.vtxz.at(vndx));
          trackVertices.push_back(vertexStream);
          trackPdgIds.push_back(htrcks.pdg.at(vndx));
          trackTrackIds.push_back(htrcks.trackid.at(vndx));
          
          
          event     = std::stoi(bxNumber);
          energy    = trackedepv.at(hittrckind);//trackedepv.at(vndx);
          time      = trtv.at(hittrckind);
          x         = trxv.at(hittrckind); //hit.cellx;
          y         = tryv.at(hittrckind); //hit.celly;
          z         = getZPosition(layer_id);
          string  s = getDetectorName(layer_id, det);
          std::strcpy(detector, s.c_str());
          pdg_code  = htrcks.pdg.at(vndx);
          track_id  = htrcks.trackid.at(vndx);
          parent_id = htrcks.ptid.at(vndx);
          double trackz = trzv.at(hittrckind);
          double trackE = htrcks.E.at(vndx);
          double vtx_x  = htrcks.vtxx.at(vndx);
          double vtx_y  = htrcks.vtxy.at(vndx);
          double vtx_z  = htrcks.vtxz.at(vndx);
          
          double p_x  = htrcks.px.at(vndx);
          double p_y  = htrcks.py.at(vndx);
          double p_z  = htrcks.pz.at(vndx);
          
          std::string energyVal = Form("%.5e",htrcks.E.at(vndx));
          trackEnergies.push_back(energyVal);
          
          std::string hitEnergyDeposition = Form("%.5e",energy);
          hitEnergies.push_back(hitEnergyDeposition);
          
          hitFileAllPix << event << " " << energy << " " << time << " " << x << " " << y << " " << z << " " << detector << " " << pdg_code << " " << track_id << " " << parent_id << " "  << layer_id << " " << det << " " << hit.cellx << " " << hit.celly << " " << trackz << " " << trackE << " " << vtx_x << " " << vtx_y << " " << vtx_z << " " << p_x << " " << p_y << " " << p_z << " " << ev_weight << " " << hit.edep << std::endl;
          
          hittrckind++;
          
        }
        
        /// remove any track coming from cerenkov or lanex
        if(trackPdgIds.size()==0)continue;
        std::string pdgIdString = "[", energyString = "[", trackIdString = "[", vertexString = "[", hitEnergyString = "[";
        
        for(size_t numberTracks = 0; numberTracks < trackPdgIds.size(); numberTracks++){
            pdgIdString     += std::to_string(trackPdgIds.at(numberTracks))+",";
            energyString    += trackEnergies.at(numberTracks)+",";
            trackIdString   += std::to_string(trackTrackIds.at(numberTracks))+",";
            vertexString    += trackVertices.at(numberTracks)+",";
            hitEnergyString += hitEnergies.at(numberTracks)+",";
        }
        
        pdgIdString          = pdgIdString.substr(0, pdgIdString.size()-1);
        pdgIdString         += "]";
        
        energyString         = energyString.substr(0, energyString.size()-1);
        energyString        += "]";
        
        trackIdString        = trackIdString.substr(0, trackIdString.size()-1);
        trackIdString       += "]";
        
        vertexString         = vertexString.substr(0, vertexString.size()-1);
        vertexString        += "]";
        
        hitEnergyString      = hitEnergyString.substr(0, hitEnergyString.size()-1);
        hitEnergyString     += "]";
        
        hitFile << bxNumber << " " << hit.hitid << " " << layer_id << " " << det << " " << hit.edep << " " << ev_weight << " " << hit.cellx << " " << hit.celly << " " << pdgIdString << " " << energyString << " " << trackIdString << " " << vertexString << " " << hitEnergyString << std::endl;
        
      }
    } //hits
    
    track_hit_map.clear();
    
    ++nev;
  }

  lhist->SaveHists(foutname);
  hitFileAllPix.close();
  hitFile.close();
  delete lhist;

//  delete hitstree;
  return 0;  
}



int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist)
{
  std::fstream  fdata;
  fdata.open(fnamelist, std::ios::in);
  if (!fdata.is_open()) {
    throw std::runtime_error(std::string("Error reding data from the file ") + fnamelist);
  }
  
  unsigned long lid = 0;
  while (!fdata.eof()) {
    std::string  ffname;
    double fweight;
    fdata >> ffname;
    if (!fdata.fail()) { 
      flist.push_back(ffname);
    }
    else if (fdata.eof()) { break; }
    else {
      std::cout << "ProcessList(..)  :  Error reading data from the file " << fnamelist 
                << ",  line: " << lid << ". Exit." << std::endl;
      fdata.close();          
      return -2;
    }
    ++lid;
  }
  
  fdata.close();

  return 0;
}  
  


void CreateHistograms(MHists *mh) 
{
  std::cout << "Creating histograms\n";

  mh->AddHists("primary_e", 3, 20000, 0.0, 20.0);
  
  //// variable binned in X axis histograms
  Double_t logmin           = -6;
  Double_t logmax           = 1;
  const Int_t nbins         = 450;
  Double_t logbinwidth      = (logmax-logmin)/nbins;
  Double_t xpoints[nbins+2] = {0.0};
  for(Int_t i=0 ; i<=nbins ; i++) xpoints[i] = TMath::Power( 10,(logmin + i*logbinwidth) );
  xpoints[451] = 2*TMath::Power( 10,1);

  int nlayers = 16;
  int nsensor = 9;
  int ndet = nsensor * nlayers;
  int npixx = 1024;
  int npixy = 512;
}


#endif

