// This works on hits and hittracks trees. It prints a text file containing the information of the hit position, energy, vertex position etc. Noam's clustering algorithm needs this information.
//

#ifndef __RUN_PROC_HITS_TREE__

void process_lxtrees_v2(const char *fnlist = 0, const char *commentstr = 0)
{
   gROOT->ProcessLineSync("#define __RUN_PROC_HITS_TREE__ 1");
   gROOT->ProcessLineSync(".L MHists.C+");
   gROOT->ProcessLineSync(".L ProcessLxSim.C+");
   gROOT->ProcessLine("#include \"process_lxtrees_v2.C\"");
   gROOT->ProcessLine(Form("process_hits_tree_draw(\"%s\")", fnlist));
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


int process_hits_tree_draw(const char *fnlist = 0, const char *commentstr = 0)
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
  std::string foutname = fnamelist.substr(fnamelist.find_last_of("/")+1);
  foutname = foutname.substr(0, foutname.find_last_of("."));
  std::string textoutname = foutname;
  foutname += suffix + std::string(".root");
  
  /// write to a text file
  ofstream hitFile;
  textoutname += std::string("_HitsProperInfo") + std::string(".txt");
  hitFile.open(textoutname);
  hitFile << "###bxNumber << hit_id << layer_id << det_id << e_dep << ev_weight << cell_x << cell_y << [pdgids] << [energies] << [trackids] << [(vx1,vy1,vz1)]" << std::endl;
  
  
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
    if (!(nev % 100000)) { std::cout << "Event " << nev << std::endl; }
    

    const auto &tracksv = lxsim->GetTracks();
    const auto voltrck = tracksv.at(0);
    const std::vector<int> &detidv = voltrck.detid;
    const auto itr = std::find (detidv.begin(), detidv.end(), -1);

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
        
        std::vector<int> ntracks_per_hits_signal(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_signal_ecut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr_ecut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_signal_zcut(ntracklayers, 0);
        std::vector<int> ntracks_per_hits_backgr_zcut(ntracklayers, 0);
        std::vector<int> trackPdgIds, trackTrackIds;
        std::vector<std::string> trackEnergies, trackVertices;
        trackPdgIds.clear(); trackTrackIds.clear(); trackEnergies.clear(); trackVertices.clear();
        int trackNumber = 0;
        //loop on hit tracks
        for (int trkid : tridlist) {
          const auto titr = std::find(htrcks.trackid.begin(), htrcks.trackid.end(), trkid);
          if (titr == htrcks.trackid.end()) {
            throw std::logic_error("Track not found in HitTracks tree!"); 
          }
          int vndx = titr - htrcks.trackid.begin();
          std::string vertexStream = Form("(%.3f,%.3f,%.3f)", htrcks.vtxx.at(vndx), htrcks.vtxy.at(vndx), htrcks.vtxz.at(vndx));
          trackVertices.push_back(vertexStream);
          lhist->FillHistW("tracking_planes_hit_track_e", layer_id, htrcks.E.at(vndx), ev_weight);
          lhist->FillHistW("tracking_planes_hit_track_proc", layer_id, htrcks.pproc.at(vndx), ev_weight);
          lhist->FillHistW("tracking_planes_hit_track_pdg", layer_id, htrcks.pdg.at(vndx), ev_weight);
          trackPdgIds.push_back(htrcks.pdg.at(vndx));
          trackTrackIds.push_back(htrcks.trackid.at(vndx));
          
          std::string energyVal = Form("%.5e",htrcks.E.at(vndx));
          trackEnergies.push_back(energyVal);
          
          if ( abs(htrcks.vtxz.at(vndx)-trzv[0]) > 0.025 ) {
            lhist->FillHistW("tracking_planes_hit_track_e_zcut", layer_id, htrcks.E.at(vndx), ev_weight);
            lhist->FillHistW("tracking_planes_hit_track_pdg_zcut", layer_id, htrcks.pdg.at(vndx), ev_weight);
            track_hit_map[htrcks.trackid.at(vndx)].push_back(hit.hitid);
          }
        }
        /// fill only when the tracks are not from the background hotspots
        lhist->FillHistW("tracking_planes_n_tracks_per_hit", detlayer, trackNumber, ev_weight);
        /// remove any track coming from cerenkov or lanex
        if(trackPdgIds.size()==0)continue;
        int bxNumber = 1;
        std::string pdgIdString = "[", energyString = "[", trackIdString = "[", vertexString = "[";        
        for(size_t numberTracks = 0; numberTracks < trackPdgIds.size(); numberTracks++){
            pdgIdString   += std::to_string(trackPdgIds.at(numberTracks))+",";
            energyString  += trackEnergies.at(numberTracks)+",";
            trackIdString += std::to_string(trackTrackIds.at(numberTracks))+",";
            vertexString  += trackVertices.at(numberTracks)+",";
        }
        pdgIdString = pdgIdString.substr(0, pdgIdString.size()-1);
        pdgIdString   += "]";
        
        energyString = energyString.substr(0, energyString.size()-1);
        energyString  += "]";
        
        trackIdString = trackIdString.substr(0, trackIdString.size()-1);
        trackIdString += "]";
        
        vertexString = vertexString.substr(0, vertexString.size()-1);
        vertexString += "]";
        
        hitFile << bxNumber << " " << hit.hitid << " " << layer_id << " " << det_id << " " << hit.edep << " " << ev_weight << " " << hit.cellx << " " << hit.celly << " " << pdgIdString << " " << energyString << " " << trackIdString << " " << vertexString << std::endl;
        
      }
    }
    
    track_hit_map.clear();
    
    ++nev;
  }
  
  hitFile.close();
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
  
  mh->AddHists("tracking_planes_n_tracks_per_hit", ndet, 1000, 0.0, 10000.0);

        
  mh->AddHists("tracking_planes_hit_track_e", nlayers, 20000, 0.0, 20.0);
  mh->AddHists("tracking_planes_hit_track_proc", nlayers, 2100, 0.0, 2100.0);
  mh->AddHists("tracking_planes_hit_track_pdg", nlayers, 100, -50.0, 50.0);
          
  mh->AddHists("tracking_planes_hit_track_e_zcut", nlayers, 20000, 0.0, 20.0);
  mh->AddHists("tracking_planes_hit_track_pdg_zcut", nlayers, 100, -50.0, 50.0);
  mh->AddHists("tracking_tracks_nhits_other", 1, 10, 0.0, 10.0);
  mh->AddHists("tracking_tracks_nhits_background", 1, 10, 0.0, 10.0);

}


#endif

