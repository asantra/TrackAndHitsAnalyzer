// this is to prepare output root file for Allpix2. This was used by Master's students. This code will be needed when we work with AllPix2 simulation. This is for signal samples. Input is the a text file containing the root file
// this is essentially copied from v4 setup, but here apart from producing text files, this code will produce root trees as well

#ifndef __RUN_PROC_HITS_TREE__

void process_lxtrees_v6(const char *fnlist = 0, std::string bxNumber=0, std::string nameOfFile = 0)
{
   gROOT->ProcessLineSync("#define __RUN_PROC_HITS_TREE__ 1");
   gROOT->ProcessLineSync(".L MHists.C+");
   gROOT->ProcessLineSync(".L ProcessLxSim.C+");
   gROOT->ProcessLine("#include \"process_lxtrees_v6.C\"");
   gROOT->ProcessLine(Form("process_hits_tree_draw(\"%s\", \"%s\", \"%s\")", fnlist, bxNumber.c_str(), nameOfFile.c_str()));
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
#include <cstring>
#include <map>

#include "TChain.h"
#include "TString.h"
#include "MHists.h"
#include "TObject.h"

using namespace std;

int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist);
void CreateHistograms(MHists *mh);

/// TDR design
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


int process_hits_tree_draw(const char *fnlist = 0, std::string bxNumber=0, std::string nameOfFile = 0)
{

  int debugl = 0; //1;

  if (!fnlist) {
    std::cout << "Usage: root -l process_lxtrees.C\'(\"file_with_list_of_mc_files\")\'\n";
    return -1;
  }
  
  std::string fnamelist(fnlist);
  std::vector<std::string>  flist;
  ProcessList(fnamelist, flist); 
  
  if (debugl) {
    std::cout << "The following files will be processed:\n";
    std::for_each(flist.begin(), flist.end(), [](const std::string ss) {std::cout << ss << std::endl;});
  }

  
  std::string suffix("_hits");
  std::string foutname = nameOfFile.substr(nameOfFile.find_last_of("/")+1);
  foutname = foutname.substr(0, foutname.find_last_of("."));
  std::string textoutname  = foutname;
  std::string textoutname2 = foutname;
  std::string rootoutname  = foutname;
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
  
  hitFileAllPix << "## event  energy  time x  y z  detector pdg_code  track_id  parent_id layer_id det hitcellx hitcelly trackz trackE vtxx vtxy vtxz p_x p_y p_z weight totalHitEDep true_type(0=purebkg/1=puresig/2=bkgfromsig)" << std::endl;
  
  
  MHists *lhist = new MHists();
  CreateHistograms(lhist);

  ProcessLxSim *lxsim = new ProcessLxSim(flist);
  
  
  int event;
  double energy;
  double time;
  double x;
  double y;
  double z;
  char detector[10];
  int pixel_id;
  int pdg_code;
  int track_id;
  int parent_id;
  int det;
  int layer_id;
  int hitcellx;
  int hitcelly;
  double trackz;
  double trackE;
  double vtxx;
  double vtxy;
  double vtxz;
  double px;
  double py;
  double pz;
  double weight;
  double hitEDep;
  int true_type;
  
  TTree *hitTree = new TTree( "hitTree", "A tree to save hits from entire tracker setup");
  hitTree->Branch("event", &event, "event/I");
  hitTree->Branch("energy", &energy, "energy/D");
  hitTree->Branch("time", &time, "time/D");
  hitTree->Branch("x", &x, "x/D");
  hitTree->Branch("y", &y, "y/D");
  hitTree->Branch("z", &z, "z/D");
  hitTree->Branch("detector", detector, "detector[10]/C");
  hitTree->Branch("pixel_id", &pixel_id, "pixel_id/I");
  hitTree->Branch("pdg_code", &pdg_code, "pdg_code/I");
  hitTree->Branch("track_id", &track_id, "track_id/I");
  hitTree->Branch("parent_id", &parent_id, "parent_id/I");
  hitTree->Branch("trackE", &trackE, "trackE/D");
  hitTree->Branch("vtxx", &vtxx, "vtxx/D");
  hitTree->Branch("vtxy", &vtxy, "vtxy/D");
  hitTree->Branch("vtxz", &vtxz, "vtxz/D");
  hitTree->Branch("px", &px, "px/D");
  hitTree->Branch("py", &py, "py/D");
  hitTree->Branch("pz", &pz, "pz/D");
  hitTree->Branch("hitcellx", &hitcellx, "hitcellx/I");
  hitTree->Branch("hitcelly", &hitcelly, "hitcelly/I");
  
  /// create a multimap of trees
  map<string, TTree*> hitTreeMap; 
  
  /// create the map 
  for(int ilyr=0; ilyr < 8; ilyr++){
        for(int ichip=0; ichip < 9; ichip++){
            string keyName = bxNumber+"_"+to_string(ilyr)+"_"+to_string(ichip);
            hitTreeMap[keyName] = hitTree;
        }
  }
  
  std::vector<int> nprimary(3,0);
  int nev = 0;
  int nrec = 1;
  while (nrec) {
    nrec = lxsim->ReadNextEvent();
    if (!nrec) continue;
    if (!(nev % 1000)) { std::cout << "Event " << nev << std::endl; }
    
    const auto &tracksv = lxsim->GetTracks();
    const auto voltrck = tracksv.at(0);
    const std::vector<int> &detidv = voltrck.detid;
    
    
    const auto itr = std::find (detidv.begin(), detidv.end(), -1);
    int primndx = -1;
    if (itr == detidv.end()) {
      std::cout << "Warning! Primary track is not found!\n";
      throw std::logic_error("Primary track is not found!");
    } else {
      primndx = itr - detidv.begin();
    }

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
        
        lhist->FillHistW("tracking_planes_hits_x", detlayer, hit.cellx, ev_weight);
        lhist->FillHistW("tracking_planes_hits_y", detlayer, hit.cellx, ev_weight);
        lhist->FillHistW("tracking_planes_hits_xy", detlayer, hit.cellx, hit.celly, ev_weight);
        lhist->FillHistW("tracking_planes_hits_xy_edep", detlayer, hit.cellx, hit.celly, hit.edep*ev_weight);
        
        lhist->FillHistW("tracking_planes_n_tracks_per_hit", layer_id, tridlist.size(), ev_weight);
        
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
          
          lhist->FillHistW("tracking_planes_hit_track_e", layer_id, htrcks.E.at(vndx), ev_weight);
          lhist->FillHistW("tracking_planes_hit_track_pdg", layer_id, htrcks.pdg.at(vndx), ev_weight);
          trackPdgIds.push_back(htrcks.pdg.at(vndx));
          trackTrackIds.push_back(htrcks.trackid.at(vndx));
          
          
          
          event         = std::stoi(bxNumber);
          energy        = trackedepv.at(hittrckind);//trackedepv.at(vndx);
          time          = trtv.at(hittrckind);
          x             = trxv.at(hittrckind); //hit.cellx;
          y             = tryv.at(hittrckind); //hit.celly;
          z             = getZPosition(layer_id);
          string  s     = getDetectorName(layer_id, det);
          std::strcpy(detector, s.c_str());
          pdg_code      = htrcks.pdg.at(vndx);
          track_id      = htrcks.trackid.at(vndx);
          parent_id     = htrcks.ptid.at(vndx);
          double evweight      = ev_weight;
          
          trackz = trzv.at(hittrckind);
          trackE = htrcks.E.at(vndx);
          vtxx  = htrcks.vtxx.at(vndx);
          vtxy  = htrcks.vtxy.at(vndx);
          vtxz  = htrcks.vtxz.at(vndx);
          px    = htrcks.px.at(vndx);
          py    = htrcks.py.at(vndx);
          pz    = htrcks.pz.at(vndx);
          true_type  = -999;
          
          
          /// need to change for g+lser processing
          if(pdg_code==-11 && track_id==1)
              true_type = 1;
          else if(track_id!=1)
              true_type = 2;
          else 
              ; 
          
          if(layer_id<8){
              hitFileAllPix << event << " " << energy << " " << time << " " << x << " " << y << " " << z << " " << detector << " " << pdg_code << " " << track_id << " " << parent_id << " "  << layer_id << " " << det << " " << hit.cellx << " " << hit.celly << " " << trackz << " " << trackE << " " << vtxx << " " << vtxy << " " << vtxz << " " << px << " " << py << " " << pz << " " << evweight << " " << hit.edep << " " << true_type << std::endl;
              /// now write to the tree map
              string key = "Stave"+to_string(layer_id)+to_string(det)+"_Event"+to_string(event);
              hitTreeMap[key]->Fill();
          }
                   
          
          
          
          std::string energyVal = Form("%.5e",htrcks.E.at(vndx));
          trackEnergies.push_back(energyVal);
          
          std::string hitEnergyDeposition = Form("%.5e",energy);
          hitEnergies.push_back(hitEnergyDeposition);
          
          if ( abs(htrcks.vtxz.at(vndx)-trzv[0]) > 0.025 ) {
            lhist->FillHistW("tracking_planes_hit_track_e_zcut", layer_id, htrcks.E.at(vndx), ev_weight);
            lhist->FillHistW("tracking_planes_hit_track_pdg_zcut", layer_id, htrcks.pdg.at(vndx), ev_weight);
            track_hit_map[htrcks.trackid.at(vndx)].push_back(hit.hitid);
          }
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
        
        if(layer_id<8) hitFile << bxNumber << " " << hit.hitid << " " << layer_id << " " << det << " " << hit.edep << " " << ev_weight << " " << hit.cellx << " " << hit.celly << " " << pdgIdString << " " << energyString << " " << trackIdString << " " << vertexString << " " << hitEnergyString << std::endl;
        
      }
    }
    track_hit_map.clear();
    
    ++nev;
  }
  
  /// now write the trees into separate root files
  for(map<string, TTree*>::iterator it=hitTreeMap.begin(); it!=hitTreeMap.end();it++){
     std::string allpixoutname = std::string("HitBranchesForAllPix_")+rootoutname+it->first+std::string(".root");
     TFile *fileOut = new TFile( allpixoutname.c_str(), "RECREATE");
     fileOut->cd();
     it->second->Write();
     fileOut->Write("", TObject::kWriteDelete);
     delete fileOut;
  }
  
  
  
  hitFile.close();
  hitFileAllPix.close();
  lhist->SaveHists(foutname);
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

  //mh->AddHists("primary_e", 3, 20000, 0.0, 20.0);

  int nlayers = 16;
  int nsensor = 9;
  int ndet = nsensor * nlayers;
  int npixx = 1024;
  int npixy = 512;
  mh->AddHists("tracking_planes_hits_x", ndet, npixx, 0.0, npixx);
  mh->AddHists("tracking_planes_hits_y", ndet, npixy, 0.0, npixy);
  mh->AddHists("tracking_planes_hits_xy", ndet, npixx, 0.0, npixx, npixy, 0.0, npixy);
  mh->AddHists("tracking_planes_hits_xy_edep", ndet, npixx, 0.0, npixx, npixy, 0.0, npixy);
  
  mh->AddHists("tracking_planes_n_tracks_per_hit", nlayers, 100, 0.0, 100.0);
        
  mh->AddHists("tracking_planes_hit_track_e", nlayers, 20000, 0.0, 20.0);
  mh->AddHists("tracking_planes_hit_track_proc", nlayers, 2100, 0.0, 2100.0);
  mh->AddHists("tracking_planes_hit_track_pdg", nlayers, 100, -50.0, 50.0);
          
  mh->AddHists("tracking_planes_hit_track_e_zcut", nlayers, 20000, 0.0, 20.0);
  mh->AddHists("tracking_planes_hit_track_pdg_zcut", nlayers, 100, -50.0, 50.0);
  mh->AddHists("tracking_tracks_nhits_other", 1, 10, 0.0, 10.0);
  mh->AddHists("tracking_tracks_nhits_background", 1, 10, 0.0, 10.0);

}


#endif

