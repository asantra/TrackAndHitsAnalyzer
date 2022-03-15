//
// This is for electron+laser signal samples, distinction in bunch crossing (taking from the evt_id==0 flag), Only prints the track info for signal. The BX is taken from the evt_id==0 flag. 
//

#ifndef __RUN_PROC_TREE__

void process_track_tree_draw_v9(const char *fnlist = 0, const char *commentstr = 0)
{
   gROOT->ProcessLineSync("#define __RUN_PROC_TREE__ 1");
   gROOT->ProcessLineSync(".L MHists.C+");
   gROOT->ProcessLine("#include \"process_track_tree_draw_v9.C\"");
   gROOT->ProcessLine(fnlist ? Form("run_process_track_tree_draw(\"%s\")", fnlist) : "run_process_track_tree_draw(0)");
   gROOT->ProcessLine("#undef __RUN_PROC_TREE__");
}

#else



int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist);

typedef std::tuple<int,int,int, double,double,double, double,double,double,double, double,double,double, double> TrckType;
//track_id, det_id, pdg, xx, yy, zz, E, pxx, pyy, pzz, vtx_x, vtx_y, vtx_z, ev_weight





int run_process_track_tree_draw(const char *fnlist = 0, const char *commentstr = 0)
{
  int debugl = 0; //1;

  if (!fnlist) {
    std::cout << "Usage: root -l process_track_tree_draw_v9.C\'(\"file_with_list_of_mc_files\")\'\n";
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
  textoutname += std::string("_trackInfo") + std::string(".txt");
  trackFile.open(textoutname);
  trackFile << "### bxNumber << pdg << track_id << det_id << xx << yy << eneg << ev_weight << vtx_x << vtx_y << vtx_z << parentid << pxx << pyy << pzz << processid << time" << std::endl;

  MHists *lhist = new MHists();
  
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
    if (!(ii % 10000)) { std::cout << "Event " << ii << std::endl;}
    
    size_t ntrck = det_idv.size();
    int primary_pdg = -99;
    int signaltracks = 0;
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
//         if (primary_pdg == 11){
//             lhist->FillHistW("primary_e_electron", 0, enegv[ii], ev_weight);
//         }
//         if (primary_pdg == 22){
//             lhist->FillHistW("primary_e_gamma", 0, enegv[ii], ev_weight);
//         }
//         /// signal positrons
//         if (primary_pdg == -11){
//             lhist->FillHistW("primary_e_positron", 0, enegv[ii], ev_weight);
//         }
      }
    }
    if(debugl)std::cout << "After getting primary particle energies" << std::endl;
    if (primary_pdg == -99) {
      std::cout << "WARNING! Primary is not found in event " << ev_id << std::endl;
    }

    for (size_t ii = 0; ii < ntrck; ++ii) {
        int det_id, pdg, track_id, parentid;
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
        parentid  = ptidv[ii];
    
        double xproj = pxx/pzz*(zproj-zz) + xx;
        double yproj = pyy/pzz*(zproj-zz) + yy;
        
        if(debugl)std::cout << "Filling up the histograms for tracking planes" << std::endl;
        /// print all det_ids, for all particles
        if(det_id >= 1000 && det_id <= 1015){
            if(det_id >=1000 && det_id<1008 && pdg==-11 && track_id==1)signaltracks++;
            trackFile << bxNumber << " " << pdg << " " << track_id << " " << det_id << " " << xx << " " << yy << " " << eneg << " " << ev_weight << " " << vtx_x << " " << vtx_y << " " << vtx_z << " " << parentid << " " << pxx << " " << pyy << " " << pzz << " " << physprocess << " " << tt << std::endl;
//         if (det_id >= 1000 && det_id <= 1015) {
//             int det = det_id - 1000;
//         /// remove unnecessary background from lanex and cherencov
//         //if(vtx_x < 0 && (vtx_z > 3600 && vtx_z < 4600))continue;
// //         /// remove photon
// //         if(pdg!=22)
// //             trackFile << bxNumber << " " << pdg << " " << track_id << " " << det_id << " " << xx << " " << yy << " " << eneg << " " << ev_weight << " " << vtx_x << " " << vtx_y << " " << vtx_z << std::endl;
// //         
//         }
        }
        // Accumulate tracks for one event 
        if (pevent == ev_id) {
            if(debugl)std::cout << "In pevent == ev_id block" << std::endl;
        } else if (pevent != ev_id) {
            if(debugl)std::cout << "In pevent != ev_id block" << std::endl;
            pevent = ev_id;
        } else { //(pevent > ev_id)
            std::cout << "New event ID is smaller than previous!\n";
            delete track_tree;
            delete lhist;
            return -1;
        }
    } //tracks loop
    std::cout << "Signal tracks " << signaltracks << endl;
  } // tree loop
  
  //closing the text file
  trackFile.close();
  
  lhist->SaveHists(foutname);
  
  delete track_tree;
  delete lhist;
  return 0;  
}




int ProcessList(const std::string &fnamelist, std::vector<std::string> &flist)
{
  std::fstream  fdata;
  fdata.open(fnamelist, std::ios::in);
  if (!fdata.is_open()) {
    throw std::runtime_error(std::string("Error reading data from the file ") + fnamelist);
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
  


#endif
