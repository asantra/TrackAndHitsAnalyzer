//
// This is for electron+laser signal samples, distinction in bunch crossing (taking from the evt_id==0 flag), only necessary for plots, better to remove the plots because they take too much of memory.

#ifndef __RUN_PROC_TREE__

void process_track_tree_draw_v6(const char *fnlist = 0, const char *commentstr = 0)
{
   gROOT->ProcessLineSync("#define __RUN_PROC_TREE__ 1");
   gROOT->ProcessLineSync(".L MHists.C+");
   gROOT->ProcessLine("#include \"process_track_tree_draw_v6.C\"");
   gROOT->ProcessLine(fnlist ? Form("run_process_track_tree_draw(\"%s\")", fnlist) : "run_process_track_tree_draw(0)");
   gROOT->ProcessLine("#undef __RUN_PROC_TREE__");
}

#else

// #include <iostream>
// #include <iomanip>
// #include <fstream>
// #include <sstream>
// #include <string>
// #include <algorithm>
// #include <stdexcept>
// #include <vector>
// #include <tuple>

// #include "TChain.h"

// #include "MHists.h"

int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist);
void CreateHistograms(MHists *mh);

typedef std::tuple<int,int,int, double,double,double, double,double,double,double, double,double,double, double> TrckType;
//track_id, det_id, pdg, xx, yy, zz, E, pxx, pyy, pzz, vtx_x, vtx_y, vtx_z, ev_weight


void TestTracks(const int evid, std::vector<TrckType> evtracks, MHists *mhist);
void TestBremsTracks(const int evid, std::vector<TrckType> evtracks, MHists *mhist);
void DumpTrack(const int evid, const TrckType &trk);



int run_process_track_tree_draw(const char *fnlist = 0, const char *commentstr = 0)
{
  int debugl = 0; //1;

  if (!fnlist) {
    std::cout << "Usage: root -l process_track_tree_draw_v6.C\'(\"file_with_list_of_mc_files\")\'\n";
    return -1;
  }
  
  
  
  std::string fnamelist(fnlist);
  std::vector<std::string>  flist;
  ProcessList(fnamelist, flist);  
  if (debugl) {
    std::cout << "The following files will be processed:\n";
    std::for_each(flist.begin(), flist.end(), [](const std::string ss) {std::cout << ss << std::endl;});
  }
  
  /// foutname is the output root file name
  std::string suffix("");
  std::string foutname = fnamelist.substr(fnamelist.find_last_of("/")+1);
  foutname = foutname.substr(0, foutname.find_last_of("."));
  std::string textoutname = foutname;
  foutname += suffix + std::string(".root");
  
  /// write to a text file
  ofstream trackFile;
  textoutname += std::string("_trackInfoClean") + std::string(".txt");
  trackFile.open(textoutname);
  trackFile << "### bxNumber << pdg << track_id << det_id << xx << yy << eneg << ev_weight << vtx_x << vtx_y << vtx_z" << std::endl;

  MHists *lhist = new MHists();
  CreateHistograms(lhist);
  if(debugl)std::cout << "After creating the histograms" << std::endl; 
  
  TChain *track_tree = new TChain("Tracks");
  std::for_each(flist.begin(), flist.end(), [track_tree](const std::string ss) {track_tree->Add(ss.c_str());} );

  double ev_weight;
  int ev_id;

  std::vector<int> det_idv, pdgv, track_idv, n_secondv, ptidv, physprocv;
  std::vector<int> *det_id_ptr = &det_idv;
  std::vector<int> *pdg_ptr = &pdgv;
  std::vector<int> *track_id_ptr = &track_idv;
  std::vector<int> *n_second_ptr = &n_secondv;
  std::vector<int> *ptid_ptr = &ptidv;
  std::vector<int> *physproc_ptr = &physprocv;

  std::vector<double> enegv, xxv, yyv, zzv, ttv, pxxv, pyyv, pzzv, vtx_xv, vtx_yv, vtx_zv;
  std::vector<double> *xx_ptr = &xxv;
  std::vector<double> *yy_ptr = &yyv;
  std::vector<double> *zz_ptr = &zzv;
  std::vector<double> *tt_ptr = &ttv;
  std::vector<double> *eneg_ptr = &enegv;
  std::vector<double> *pxx_ptr = &pxxv;
  std::vector<double> *pyy_ptr = &pyyv;
  std::vector<double> *pzz_ptr = &pzzv;
  std::vector<double> *vtx_x_ptr = &vtx_xv;
  std::vector<double> *vtx_y_ptr = &vtx_yv;
  std::vector<double> *vtx_z_ptr = &vtx_zv;
  
  track_tree->SetBranchAddress("eventid", &ev_id);
  track_tree->SetBranchAddress("weight", &ev_weight);
  track_tree->SetBranchAddress("detid", &det_id_ptr);
  track_tree->SetBranchAddress("pdg", &pdg_ptr);
  track_tree->SetBranchAddress("trackid", &track_id_ptr);
  track_tree->SetBranchAddress("x", &xx_ptr);
  track_tree->SetBranchAddress("y", &yy_ptr);
  track_tree->SetBranchAddress("z", &zz_ptr);
  track_tree->SetBranchAddress("t", &tt_ptr);
  track_tree->SetBranchAddress("E",  &eneg_ptr);
  track_tree->SetBranchAddress("px", &pxx_ptr);
  track_tree->SetBranchAddress("py", &pyy_ptr);
  track_tree->SetBranchAddress("pz", &pzz_ptr);
  track_tree->SetBranchAddress("vtxx", &vtx_x_ptr);
  track_tree->SetBranchAddress("vtxy", &vtx_y_ptr);
  track_tree->SetBranchAddress("vtxz", &vtx_z_ptr);
  track_tree->SetBranchAddress("physproc", &physproc_ptr);
  track_tree->SetBranchAddress("ptrackid", &ptid_ptr);
  track_tree->SetBranchAddress("nsecondary", &n_second_ptr);

  const double ipmagcutx = 165.0; 
  const double ipmagcuty = 54.0; 
  const double zproj = 2748.0;

  std::vector<TrckType> event_tracks;
  int pevent = -1;
  int nevproc = track_tree->GetEntries();
  if(true)std::cout << "Total number of events: " << nevproc << std::endl;
  int bxNumber = 0; /// bunch crossing number
  
  
  for (Long64_t ii = 0; ii < nevproc; ++ii) {
    track_tree->GetEntry(ii);
//     if (eneg < 1.0) continue;
    if(debugl)std::cout << "Inside the loop. Processing " << ii << std::endl;
    if (!(ii % 1000000)) { std::cout << "Event " << ii << std::endl;}
    //if (ii > 20000000)break;
    
    size_t ntrck = det_idv.size();
    int primary_pdg = -99;
    /// count bunch crossing
    if(ev_id==0){
       bxNumber++;  
    }
    for (size_t ii = 0; ii < ntrck; ++ii) {
      double zproj = 2748.0;
      double xproj = pxxv[ii]/pzzv[ii]*(zproj-zzv[ii]) + xxv[ii];
      double yproj = pyyv[ii]/pzzv[ii]*(zproj-zzv[ii]) + yyv[ii];
      if (det_idv[ii] == -1) {
        primary_pdg = pdgv[ii];
        if (primary_pdg == 11){
            lhist->FillHistW("primary_e_electron", 0, enegv[ii], ev_weight);
        }
        if (primary_pdg == 22){
            lhist->FillHistW("primary_e_gamma", 0, enegv[ii], ev_weight);
        }
        /// signal positrons
        if (primary_pdg == -11){
            lhist->FillHistW("primary_e_positron", 0, enegv[ii], ev_weight);
        }
      }
    }
    if(debugl)std::cout << "After getting primary particle energies" << std::endl;
//     if (primary_pdg == -99) {
//       std::cout << "WARNING! Primary is not found in event " << ev_id << std::endl;
//     }

  for (size_t ii = 0; ii < ntrck; ++ii) {
    int det_id, pdg, track_id;
    det_id = det_idv[ii];
    pdg = pdgv[ii];
    track_id = track_idv[ii];
      
    double eneg, xx, yy, zz, tt, pxx, pyy, pzz, vtx_x, vtx_y, vtx_z, physprocess;
    eneg = enegv[ii];
    xx = xxv[ii];
    yy = yyv[ii];
    zz = zzv[ii];
    tt = ttv[ii];
    pxx = pxxv[ii];
    pyy = pyyv[ii];
    pzz = pzzv[ii];
    vtx_x = vtx_xv[ii];
    vtx_y = vtx_yv[ii];
    vtx_z = vtx_zv[ii];
    physprocess = physprocv[ii];
  
    double xproj = pxx/pzz*(zproj-zz) + xx;
    double yproj = pyy/pzz*(zproj-zz) + yy;
    
    if(debugl)std::cout << "Filling up the histograms for tracking planes" << std::endl;
    if (det_id >= 1000 && det_id <= 1015) {
      int det = det_id - 1000;
      /// remove unnecessary background from lanex and cherencov
      //if(vtx_x < 0 && (vtx_z > 3600 && vtx_z < 4600))continue;
      /// remove photon
      if(pdg!=22)
          trackFile << bxNumber << " " << pdg << " " << track_id << " " << det_id << " " << xx << " " << yy << " " << eneg << " " << ev_weight << " " << vtx_x << " " << vtx_y << " " << vtx_z << std::endl;
      
      
      if (pdg == 11)  {
//           lhist->FillHistW("tracking_planes_track_x_electrons", det, xx, ev_weight);
//           lhist->FillHistW("tracking_planes_track_x_electrons_sumE", det, xx, ev_weight*eneg);
//           if(eneg>1.0)lhist->FillHistW("tracking_planes_track_x_electrons_1GeVCut", det, xx, ev_weight);
          if(track_id!=1){
            //multiplicityBackgroundEle[bxNumber][det]++;
            lhist->FillHistW("tracking_planes_background_track_x_electrons", det, xx, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_y_electrons", det, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_track_x_electrons_sumE", det, xx, ev_weight*eneg);
            lhist->FillHistW("tracking_planes_background_track_e_electrons_log", det, eneg, ev_weight); 
            lhist->FillHistW("tracking_planes_background_vtx_z_track_e_electrons_log", det, vtx_z, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtx_x_track_e_electrons_log", det, vtx_x, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_y_track_e_electrons_log", det, vtx_y, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_x_track_e_electrons_log", det, xx, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_z_electrons", det, vtx_z, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_xy_electrons", det, xx, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtxz_vtxx_electrons", det, vtx_z, vtx_x, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxz_vtxy_electrons", det, vtx_z, vtx_y, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxx_vtxy_electrons", det, vtx_x, vtx_y, ev_weight);
        }
      }
      
      if (pdg == -11)  {
//           lhist->FillHistW("tracking_planes_track_x_positrons", det, xx, ev_weight);
//           lhist->FillHistW("tracking_planes_track_x_positrons_sumE", det, xx, ev_weight*eneg);
//           if(eneg>1.0)lhist->FillHistW("tracking_planes_track_x_positrons_1GeVCut", det, xx, ev_weight);
          if(track_id==1){
            lhist->FillHistW("tracking_planes_signal_track_x_positrons", det, xx, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_track_y_positrons", det, yy, ev_weight);
            lhist->FillHistW("tracking_planes_signal_track_x_positrons_sumE", det, xx, ev_weight*eneg);
            lhist->FillHistW("tracking_planes_signal_track_e_positrons_log", det, eneg, ev_weight); 
            lhist->FillHistW("tracking_planes_signal_vtx_z_track_e_positrons_log", det, vtx_z, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_signal_vtx_x_track_e_positrons_log", det, vtx_x, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_vtx_y_track_e_positrons_log", det, vtx_y, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_track_x_track_e_positrons_log", det, xx, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_vtx_z_positrons", det, vtx_z, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_track_xy_positrons", det, xx, yy, ev_weight);
            lhist->FillHistW("tracking_planes_signal_vtxz_vtxx_positrons", det, vtx_z, vtx_x, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_vtxz_vtxy_positrons", det, vtx_z, vtx_y, ev_weight);
//             lhist->FillHistW("tracking_planes_signal_vtxx_vtxy_positrons", det, vtx_x, vtx_y, ev_weight);
        }
        if(track_id!=1){
            lhist->FillHistW("tracking_planes_background_track_x_positrons", det, xx, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_y_positrons", det, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_track_x_positrons_sumE", det, xx, ev_weight*eneg);
            lhist->FillHistW("tracking_planes_background_track_e_positrons_log", det, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtx_z_track_e_positrons_log", det, vtx_z, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtx_x_track_e_positrons_log", det, vtx_x, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_y_track_e_positrons_log", det, vtx_y, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_x_track_e_positrons_log", det, xx, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_z_positrons", det, vtx_z, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_xy_positrons", det, xx, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtxz_vtxx_positrons", det, vtx_z, vtx_x, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxz_vtxy_positrons", det, vtx_z, vtx_y, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxx_vtxy_positrons", det, vtx_x, vtx_y, ev_weight);
        }
      }
      if (pdg == 22)  {
//           lhist->FillHistW("tracking_planes_track_x_gamma", det, xx, ev_weight);
//           lhist->FillHistW("tracking_planes_track_x_gamma_sumE", det, xx, ev_weight*eneg);
//           if(eneg>1.0)lhist->FillHistW("tracking_planes_track_x_gamma_1GeVCut", det, xx, ev_weight);
          if(track_id!=1){
            lhist->FillHistW("tracking_planes_background_track_x_gamma", det, xx, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_y_gamma", det, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_track_x_gamma_sumE", det, xx, ev_weight*eneg);
            lhist->FillHistW("tracking_planes_background_track_e_gamma_log", det, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtx_z_track_e_gamma_log", det, vtx_z, eneg, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtx_x_track_e_gamma_log", det, vtx_x, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_y_track_e_gamma_log", det, vtx_y, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_x_track_e_gamma_log", det, xx, eneg, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtx_z_gamma", det, vtx_z, ev_weight);
//             lhist->FillHistW("tracking_planes_background_track_xy_gamma", det, xx, yy, ev_weight);
            lhist->FillHistW("tracking_planes_background_vtxz_vtxx_gamma", det, vtx_z, vtx_x, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxz_vtxy_gamma", det, vtx_z, vtx_y, ev_weight);
//             lhist->FillHistW("tracking_planes_background_vtxx_vtxy_gamma", det, vtx_x, vtx_y, ev_weight);
        }
      }
    }
    
    // Accumulate tracks for one event 
    if (pevent == ev_id) {
      if(debugl)std::cout << "In pevent == ev_id block" << std::endl;
      //event_tracks.push_back(std::make_tuple(track_id, det_id, pdg, xx, yy, zz,eneg, pxx, pyy, pzz, vtx_x, vtx_y, vtx_z, ev_weight));
    } else if (pevent != ev_id) {
      if(debugl)std::cout << "In pevent != ev_id block" << std::endl;
//       TestTracks(pevent, event_tracks, lhist);
//       TestBremsTracks(pevent, event_tracks, lhist);
      //event_tracks.clear();
      //event_tracks.push_back(std::make_tuple(track_id, det_id, pdg, xx, yy, zz, eneg, pxx, pyy, pzz, vtx_x, vtx_y, vtx_z, ev_weight));
      pevent = ev_id;
    } else { //(pevent > ev_id)
      std::cout << "New event ID is smaller than previous!\n";
      delete track_tree;
      delete lhist;
      return -1;
    }
  } //tracks loop
  } // tree loop
  
  //closing the text file
  trackFile.close();
    
 //*********************To draw histos
//  lhist->DrawHist1D_BT15("tracking_planes_track_x");

//    lhist->DrawHist2D_BT15("ip_n_gamma_n_electrons_scint", "ip_n_gamma_n_electrons_scint", "N_gamma", "N_e", "N", "colz");
  

  double binw(1.0), nbx = 1.00;//flist.size();
  std::cout << "Number of BX: " << nbx << std::endl;
  
  /// normalizing to BX
  std::vector<std::string> pprimet{"primary_e_electron", "primary_e_gamma", "primary_e_positron"};
  TH1* hhbw = lhist->GetHist(pprimet.front(), 0);
  if (hhbw) binw = hhbw->GetBinWidth(1); else std::cerr << "Error to get E bin width. Can not normilaze!\n";
  for_each(pprimet.begin(), pprimet.end(), [=, &lhist](const std::string hhs) {lhist->Scale(hhs, 1.0/nbx/binw);});
  TCanvas *c0 = lhist->DrawHist1DCmp(pprimet, "MC spectra", "E (GeV)", "dN/dE per BX");
  lhist->SetLog(c0);
//   std::vector<std::string> cesige{"primary_e_electron", "ce_cherenkov_e_signal", "ce_cherenkov_e_electrons",
//                                   "ce_cherenkov_e_positrons"};
//   for_each(cesige.begin()+1, cesige.end(), [=, &lhist](const std::string hhs) {lhist->Scale(hhs, 1.0/nbx/binw);});
//   TCanvas *c1 = lhist->DrawHist1DCmp(cesige, "Spectra", "E (GeV)", "dN/dE per BX");
//   lhist->SetLog(c1);
// 
//   std::vector<std::string> cesigx{"ce_cherenkov_x_signal", "ce_cherenkov_x_electrons", "ce_cherenkov_x_positrons"};
//   double binwx(1.0);
//   hhbw = lhist->GetHist(cesigx.front(), 0);
//   if (hhbw) binwx = hhbw->GetBinWidth(1); else std::cerr << "Error to get X bin width. Can not normilaze!\n";
//   for_each(cesigx.begin(), cesigx.end(), [=, &lhist](const std::string hhs) {lhist->Scale(hhs, 1.0/nbx/binwx);});
//   TCanvas *c2 = lhist->DrawHist1DCmp(cesigx, "Position", "X (mm)", "dN/dX per BX");
//   lhist->SetLog(c2);
  
  
  /// normalizing 1D plots to BX, tracker plots
//   std::vector<std::string> trackerPlot{
  //// these are needed for filling up the spreadsheet
//   "tracking_planes_track_x_positrons",
//   "tracking_planes_track_x_positrons_sumE",
//   "tracking_planes_track_x_positrons_1GeVCut",
//   "tracking_planes_track_x_electrons",
//   "tracking_planes_track_x_electrons_sumE",
//   "tracking_planes_track_x_electrons_1GeVCut",
//   "tracking_planes_track_x_gamma",
//   "tracking_planes_track_x_gamma_sumE",
//   "tracking_planes_track_x_gamma_1GeVCut",
//   "tracking_planes_signal_track_x_positrons", 
//   "tracking_planes_signal_track_x_positrons_sumE", 
//   /*"tracking_planes_signal_track_y_positrons",*/ 
//   "tracking_planes_signal_track_e_positrons_log", 
//   "tracking_planes_signal_vtx_z_track_e_positrons_log",
//   "tracking_planes_signal_vtx_x_track_e_positrons_log",
// //   "tracking_planes_signal_vtx_y_track_e_positrons_log",
// //   "tracking_planes_signal_track_x_track_e_positrons_log",
// //   "tracking_planes_signal_vtx_z_positrons", 
// //   "tracking_planes_signal_track_xy_positrons", 
//   "tracking_planes_signal_vtxz_vtxx_positrons", 
// //   "tracking_planes_signal_vtxz_vtxy_positrons", 
// //   "tracking_planes_signal_vtxx_vtxy_positrons",
//   "tracking_planes_background_track_x_positrons", 
//   "tracking_planes_background_track_x_positrons_sumE",
// //   "tracking_planes_background_track_y_positrons", 
//   "tracking_planes_background_track_e_positrons_log", 
//   "tracking_planes_background_vtx_z_track_e_positrons_log",
//   "tracking_planes_background_vtx_x_track_e_positrons_log",
// //   "tracking_planes_background_vtx_y_track_e_positrons_log",
// //   "tracking_planes_background_track_x_track_e_positrons_log",
//   "tracking_planes_background_vtx_z_positrons", 
//   "tracking_planes_background_track_xy_positrons", 
//   "tracking_planes_background_vtxz_vtxx_positrons", 
//   "tracking_planes_background_vtxz_vtxy_positrons", 
//   "tracking_planes_background_vtxx_vtxy_positrons",
//   "tracking_planes_background_track_x_electrons",
//   "tracking_planes_background_track_x_electrons_sumE",
//   "tracking_planes_background_track_y_electrons", 
//   "tracking_planes_background_track_e_electrons_log",
//   "tracking_planes_background_vtx_z_track_e_electrons_log",
//   "tracking_planes_background_vtx_x_track_e_electrons_log",
//   "tracking_planes_background_vtx_y_track_e_electrons_log",
//   "tracking_planes_background_track_x_track_e_electrons_log",
//   "tracking_planes_background_vtx_z_electrons", 
//   "tracking_planes_background_track_xy_electrons", 
//   "tracking_planes_background_vtxz_vtxx_electrons", 
//   "tracking_planes_background_vtxz_vtxy_electrons", 
//   "tracking_planes_background_vtxx_vtxy_electrons",
//   "tracking_planes_background_track_x_gamma", 
//   "tracking_planes_background_track_y_gamma", 
//   "tracking_planes_background_track_e_gamma_log",
//   "tracking_planes_background_track_x_gamma_sumE",
//   "tracking_planes_background_vtx_z_track_e_gamma_log",
//   "tracking_planes_background_vtx_x_track_e_gamma_log",
//   "tracking_planes_background_vtx_y_track_e_gamma_log",
//   "tracking_planes_background_track_x_track_e_gamma_log",
//   "tracking_planes_background_vtx_z_gamma", 
//   "tracking_planes_background_track_xy_gamma", 
//   "tracking_planes_background_vtxz_vtxx_gamma", 
//   "tracking_planes_background_vtxz_vtxy_gamma", 
//   "tracking_planes_background_vtxx_vtxy_gamma",
//   "tracking_planes_background_track_e_gamma_log",
//   "tracking_planes_background_track_e_positrons_log",
//   "tracking_planes_background_track_e_electrons_log"};
//   
//   for_each(trackerPlot.begin(), trackerPlot.end(), [=, &lhist](const std::string hhs) {lhist->Scale(hhs, 1.0/nbx);}); // 1.0/nbx/binwtrackx
//   hhbw = lhist->GetHist(trackerx.front(), 0);
//   double binwtrackx(1.0);
//   if (hhbw) binwtrackx = hhbw->GetBinWidth(1); else std::cerr << "Error to get X bin width. Can not normilaze!\n";
//   print the integral of the histograms
  if(debugl)std::cout << "After Bx normalization" << std::endl;
  
  lhist->SaveHists(foutname);
  
  delete track_tree;
  delete lhist;
  return 0;  
}



void TestTracks(const int evid, std::vector<TrckType> evtracks, MHists *mhist)
{
//   DumpTrack(evid, trk);
  std::stable_sort(evtracks.begin(), evtracks.end(), [](TrckType x, TrckType y) {if (std::get<0>(x) < std::get<0>(y)) 
                                                                                 return true; else return false;} );
  std::map<int, int> track_count;
  int ltid = -100;
  int tcount = 0;
  for (const auto &trk : evtracks) {
//     std::cout << "Sorted Track id: " << std::get<0>(trk) << " det id: " << std::get<1>(trk) << std::endl;
    int detid = std::get<1>(trk);
//     if (detid == 2000 || detid == 2001) DumpTrack(evid, trk);
    if (detid < 1000 || detid > 1015) continue;
    int trackid = std::get<0>(trk);
    if (trackid == ltid) {
      ++tcount;  
    } else {
      if (ltid > 0) {
        track_count[ltid] = tcount; 
        mhist->FillHistW("tracking_planes_n_track_cross", 0, tcount, std::get<13>(trk));  
      }
      ltid = trackid;
      tcount = 1;
    }
  }
  
  const double ipmagcutx = 165.0; 
  const double ipmagcuty = 54.0; 
  const double zproj = 2748.0;
  
  int ntrckmax = 3;
  for (const auto &tid : track_count) {
    if (tid.second >= ntrckmax) {
      for (const auto &trk : evtracks) {
        int detid = std::get<1>(trk);
        if (detid < 1000 || detid > 1015) continue;
        int trackid = std::get<0>(trk);
        if (trackid == tid.first) {
          int pdg = std::get<2>(trk);
          int det = detid-1000;
          if (pdg==11 || pdg==-11) {
            double xx = std::get<3>(trk);
            double yy = std::get<4>(trk);
            double zz = std::get<5>(trk);
            double pxx = std::get<7>(trk);
            double pyy = std::get<8>(trk);
            double pzz = std::get<9>(trk);
            double ev_weight = std::get<13>(trk);
            mhist->FillHistW("tracking_planes_track_xy_charged_tracks", det, xx, yy, ev_weight);
            
            double xproj = pxx/pzz*(zproj-zz) + xx;
            double yproj = pyy/pzz*(zproj-zz) + yy;
            if (fabs(xproj) < ipmagcutx && fabs(yproj) < ipmagcuty) {
              mhist->FillHistW("tracking_planes_track_xy_charged_tracks_cut", det, xx, yy, ev_weight);
            }
          }
        }
      }
    }
  }
  
}



void TestBremsTracks(const int evid, std::vector<TrckType> evtracks, MHists *mhist)
{
//   DumpTrack(evid, trk);
//   std::stable_sort(evtracks.begin(), evtracks.end(), [](TrckType x, TrckType y) {if (std::get<0>(x) < std::get<0>(y)) 
//                                                                                  return true; else return false;} );
  int ip_n_gamma = 0;
  int ip_n_gamma_ecut = 0;
  int scint_n_e = 0;
  int cher_n_e = 0;
  double ev_weight = 0.0;
  double egamma = 0.0;
  double ecut = 7.0;
  for (const auto &trk : evtracks) {
//     std::cout << "Sorted Track id: " << std::get<0>(trk) << " det id: " << std::get<1>(trk) << std::endl;
    int detid = std::get<1>(trk);
    int pdg = std::get<2>(trk);
    if (detid == 5000 && pdg==22) { 
      ++ip_n_gamma; 
      ev_weight = std::get<13>(trk);
      egamma = std::get<6>(trk);
      if (egamma > ecut) ++ip_n_gamma_ecut; 
    }
    if (detid == 6000 && pdg==11) ++scint_n_e;
    if (detid == 6100 && pdg==11) ++cher_n_e;
  }

  mhist->FillHistW("ip_n_gamma_n_electrons_scint", 0, ip_n_gamma, scint_n_e, ev_weight);
  mhist->FillHistW("ip_n_gamma_n_electrons_cherenkov", 0, ip_n_gamma, cher_n_e, ev_weight);
  mhist->FillHistW("ip_n_gamma_7gev_n_electrons_scint", 0, ip_n_gamma_ecut, scint_n_e, ev_weight);
  mhist->FillHistW("ip_e_gamma_7gev_n_electrons_cherenkov", 0, ip_n_gamma_ecut, cher_n_e, ev_weight);

  if (ip_n_gamma == 1) {
    for (const auto &trk : evtracks) {
      int detid = std::get<1>(trk);
      int pdg = std::get<2>(trk);
      if (detid == 6000 && pdg==11) {
        double yy = std::get<4>(trk);
        mhist->FillHistW("ip_e_gamma_y_electrons_scint", 0, yy, egamma, ev_weight);
      }
      if (detid == 6100 && pdg==11) {
        double yy = std::get<4>(trk);
        mhist->FillHistW("ip_e_gamma_y_electrons_cherenkov", 0, yy, egamma, ev_weight);
      }
    }
  }
}



void DumpTrack(const int evid, const TrckType &trk)
{
 std::cout << "Event: " << evid << "  ";
   std::cout << "Track (id / det_id / pdg / E / xyz / p_xyz / vtx_xyz/ w /:" 
             << "  " << std::get<0>(trk) 
             << "  " << std::get<1>(trk)
             << "  " << std::get<2>(trk)
             << "  " << std::get<6>(trk)
             << "  " << std::get<3>(trk)
             << "  " << std::get<4>(trk)
             << "  " << std::get<5>(trk)
             << "  " << std::get<7>(trk)
             << "  " << std::get<8>(trk)
             << "  " << std::get<9>(trk)
             << "  " << std::get<10>(trk)
             << "  " << std::get<11>(trk)
             << "  " << std::get<12>(trk)
             << "  " << std::get<13>(trk) << std::endl;
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
//       std::cout << "File name " << ffname << " is read from the list file" << std::endl;
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
  int ndet = 16;
  bool debugCH = true;
  /// general plots
  
  /// signal positrons
  
  
  mh->AddHists("tracking_planes_signal_track_x_positrons", ndet, 1300, -650.0, 650.0);
  mh->AddHists("tracking_planes_signal_track_x_positrons_sumE", ndet, 1300, -650.0, 650.0);
//   mh->AddHists("tracking_planes_signal_track_y_positrons", ndet, 2000, -25.0, 25.0);
//   mh->AddHists("tracking_planes_signal_vtx_z_positrons", ndet, 2000, -5000, 15000);
//   mh->AddHists("tracking_planes_signal_track_xy_positrons", ndet, 1300, -650.0, 650.0, 50, -25.0, 25.0);
  mh->AddHists("tracking_planes_signal_vtxz_vtxx_positrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_signal_vtxz_vtxy_positrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_signal_vtxx_vtxy_positrons", ndet, 6000, -3000, 3000, 6000, -3000, 3000);
  
  
  
  if(debugCH)std::cout << "Created signal positrons plots" << std::endl;
  
  /// background positrons
  mh->AddHists("tracking_planes_background_track_x_positrons", ndet, 1300, -650, 650);
  mh->AddHists("tracking_planes_background_track_x_positrons_sumE", ndet, 1300, -650, 650);
//   mh->AddHists("tracking_planes_background_track_y_positrons", ndet, 2000, -25, 25);
//   mh->AddHists("tracking_planes_background_vtx_z_positrons", ndet, 2000, -5000, 15000);
//   mh->AddHists("tracking_planes_background_track_xy_positrons", ndet, 1300, -650, 650, 50, -25, 25);
  mh->AddHists("tracking_planes_background_vtxz_vtxx_positrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxz_vtxy_positrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxx_vtxy_positrons", ndet, 6000, -3000, 3000, 6000, -3000, 3000);
  
  
  if(debugCH)std::cout << "Created general background plots" << std::endl;
  
  
  /// background electrons
  
  mh->AddHists("tracking_planes_background_track_x_electrons", ndet, 1300, -650, 650);
  mh->AddHists("tracking_planes_background_track_x_electrons_sumE", ndet, 1300, -650, 650);
//   mh->AddHists("tracking_planes_background_track_y_electrons", ndet, 200, -25, 25);
//   mh->AddHists("tracking_planes_background_vtx_z_electrons", ndet, 2000, -5000, 15000);
//   mh->AddHists("tracking_planes_background_track_xy_electrons", ndet, 1300, -650, 650, 50, -25, 25);
  mh->AddHists("tracking_planes_background_vtxz_vtxx_electrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxz_vtxy_electrons", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxx_vtxy_electrons", ndet, 6000, -3000, 3000, 6000, -3000, 3000);
  
  
  if(debugCH)std::cout << "Created background electron plots" << std::endl;
  
  /// background gamma
//   mh->AddHists("tracking_planes_track_x_gamma", ndet, 1300, -650.0, 650.0);
//   mh->AddHists("tracking_planes_track_x_gamma_sumE", ndet, 1300, -650.0, 650.0);
//   mh->AddHists("tracking_planes_track_x_gamma_1GeVCut",ndet, 1300, -650.0, 650.0);
  mh->AddHists("tracking_planes_background_track_x_gamma", ndet, 1300, -650, 650);
  mh->AddHists("tracking_planes_background_track_x_gamma_sumE", ndet, 1300, -650, 650);
//   mh->AddHists("tracking_planes_background_track_y_gamma", ndet, 200, -25, 25);
//   mh->AddHists("tracking_planes_background_vtx_z_gamma", ndet, 2000, -5000, 15000);
//   mh->AddHists("tracking_planes_background_track_xy_gamma", ndet, 1300, -650, 650, 50, -25, 25);
  mh->AddHists("tracking_planes_background_vtxz_vtxx_gamma", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxz_vtxy_gamma", ndet, 2000, -5000, 15000, 6000, -3000, 3000);
//   mh->AddHists("tracking_planes_background_vtxx_vtxy_gamma", ndet, 6000, -3000, 3000, 6000, -3000, 3000);
  
  
  //// variable binned in X axis histograms
  Double_t logmin           = -6;
  Double_t logmax           = 1;
  const Int_t nbins         = 450;
  Double_t logbinwidth      = (logmax-logmin)/nbins;
  Double_t xpoints[nbins+2] = {0.0};
  for(Int_t i=0 ; i<=nbins ; i++) xpoints[i] = TMath::Power( 10,(logmin + i*logbinwidth) );
  xpoints[451] = 2*TMath::Power( 10,1);
  
  
  mh->AddHistsLogBin("tracking_planes_signal_track_e_positrons_log", ndet, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_track_e_gamma_log", ndet, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_track_e_electrons_log", ndet, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_track_e_positrons_log", ndet, nbins+1, xpoints);
  
  mh->AddHistsLogBin("tracking_planes_background_vtx_z_track_e_gamma_log", ndet, 2000, -5000, 15000, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_vtx_x_track_e_gamma_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_vtx_y_track_e_gamma_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_track_x_track_e_gamma_log", ndet, 1300, -650, 650, nbins+1, xpoints);
  
  
  mh->AddHistsLogBin("tracking_planes_background_vtx_z_track_e_electrons_log", ndet, 2000, -5000, 15000, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_vtx_x_track_e_electrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_vtx_y_track_e_electrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_track_x_track_e_electrons_log", ndet, 1300, -650, 650, nbins+1, xpoints);
  
  mh->AddHistsLogBin("tracking_planes_background_vtx_z_track_e_positrons_log", ndet, 2000, -5000, 15000, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_background_vtx_x_track_e_positrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_vtx_y_track_e_positrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_background_track_x_track_e_positrons_log", ndet, 1300, -650, 650, nbins+1, xpoints);
  
  mh->AddHistsLogBin("tracking_planes_signal_vtx_z_track_e_positrons_log", ndet, 2000, -5000, 15000, nbins+1, xpoints);
  mh->AddHistsLogBin("tracking_planes_signal_vtx_x_track_e_positrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_signal_vtx_y_track_e_positrons_log", ndet, 6000, -3000, 3000, nbins+1, xpoints);
//   mh->AddHistsLogBin("tracking_planes_signal_track_x_track_e_positrons_log", ndet, 1300, -650, 650, nbins+1, xpoints);
 
  if(debugCH)std::cout << "Created background gamma plots" << std::endl;
  
  ndet = 1; //6300
  mh->AddHists("primary_e_electron", ndet, 200, 0.0, 20.0);
  mh->AddHists("primary_e_positron", ndet, 200, 0.0, 20.0);
  mh->AddHists("primary_e_gamma", ndet, 200, 0.0, 20.0);
}

#endif
