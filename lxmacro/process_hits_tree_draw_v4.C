//// this is only working to print the hits, their cell_x, cell_y etc. Not much of a help since Noam's clustering algorithm needs more information

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm>
#include <stdexcept>
#include <limits>
#include <math.h>
#include "TMath.h"
#include "TH1.h"
#include <chrono>
#include "TChain.h"

int process_hits_tree_draw_v4(const std::string ss, std::string bxNumber)
{
    
  int debugl = 0; //1;
  
  /// output root file
  std::string suffix("_hits");
  std::string foutname = "list_root_hics_165gev_w0_3000nm_WIS";
  std::string textoutname = foutname;
  foutname += suffix + std::string(".root");
  /// write to a text file
  ofstream hitFile;
  textoutname += std::string("_HitsInfo") + std::string(".txt");
  hitFile.open(textoutname, fstream::in | fstream::out | fstream::app);
   
  TChain *hitstree = new TChain("Hits");
  hitstree->Add(ss.c_str());

  double e_dep, ev_weight;
  int det_id, ev_id, layer_id, hit_id, cell_x, cell_y;
  std::vector<int> track_list;
  std::vector<double> track_x, track_y, track_z;

  std::vector<int> *track_list_p = &track_list;
  std::vector<double> *track_x_p = &track_x; 
  std::vector<double> *track_y_p = &track_y;
  std::vector<double> *track_z_p = &track_z;

  hitstree->SetBranchAddress("eventid", &ev_id);
  hitstree->SetBranchAddress("detid", &det_id);
  hitstree->SetBranchAddress("layerid", &layer_id);
  hitstree->SetBranchAddress("hitid", &hit_id);
  hitstree->SetBranchAddress("cellx", &cell_x);
  hitstree->SetBranchAddress("celly", &cell_y);
  hitstree->SetBranchAddress("edep",  &e_dep);
  hitstree->SetBranchAddress("weight", &ev_weight);
  hitstree->SetBranchAddress("track_list", &track_list_p);
  hitstree->SetBranchAddress("trackx", &track_x_p);
  hitstree->SetBranchAddress("tracky", &track_y_p);
  hitstree->SetBranchAddress("trackz", &track_z_p);
  
  const double ipmagcutx = 165.0; 
  const double ipmagcuty = 54.0; 
  const double zproj = 2748.0;

  Long64_t nevproc = hitstree->GetEntries();
  if(debugl)std::cout << "After the assignment of the trees. Entries: " << nevproc << std::endl;
  for (Long64_t ii = 0; ii < nevproc; ++ii) {
    hitstree->GetEntry(ii);
    
    if (!(ii % 100)) { std::cout << "Event " << ii << std::endl; }
    if(debugl)std::cout << "Inside the loop, processing: " << ii << std::endl;
    if (det_id >= 1000 && det_id <= 1008) {
      const int nlayers = 16;  
      int det = det_id - 1000;
      int detlayer = det * nlayers + layer_id;
      hitFile << bxNumber << " " << hit_id << " " << layer_id << " " << det_id << " " << e_dep << " " << ev_weight << " " << cell_x << " " << cell_y << std::endl;
    }
  } // tree loop
 //closing the text file
  hitFile.close();

  return 0;  
}





