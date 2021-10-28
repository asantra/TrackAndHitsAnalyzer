//
//

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
#include "TFile.h"

#include "ProcessLxSim.h"
#include "MHists.h"


// LxHits
/////////////////////////////////////////////////////////////////////////
LxHits::LxHits(): eventid(-1), detid(0), layerid(0),
cellx(0.0), celly(0.0), edep(0.0), hitid(0), track_list(0), trackx(0), tracky(0), trackz(0), weight(0.0)
{};


LxHits::LxHits(const LxHits &hit): eventid(hit.eventid), detid(hit.detid), layerid(hit.layerid),
cellx(hit.cellx), celly(hit.celly), edep(hit.edep), hitid(hit.hitid), 
track_list(hit.track_list), trackx(hit.trackx), tracky(hit.tracky), trackz(hit.trackz), weight(hit.weight)
{};
   

LxHits::~LxHits()
{};


// LxHitsTree
/////////////////////////////////////////////////////////////////////////
LxHitsTree::LxHitsTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
     throw std::invalid_argument("LxHitsTree::LxHitsTree TTree is null!");  
   }
   Init(tree);
}


LxHitsTree::~LxHitsTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}


Int_t LxHitsTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}


Long64_t LxHitsTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void LxHitsTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
//    track_list = 0;
//    trackx = 0;
//    tracky = 0;
//    trackz = 0;
   track_list_ptr = &track_list;
   trackx_ptr = &trackx;
   tracky_ptr = &tracky;
   trackz_ptr = &trackz;

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("eventid", &eventid, &b_eventid);
   fChain->SetBranchAddress("detid", &detid, &b_detid);
   fChain->SetBranchAddress("layerid", &layerid, &b_layerid);
   fChain->SetBranchAddress("cellx", &cellx, &b_cellx);
   fChain->SetBranchAddress("celly", &celly, &b_celly);
   fChain->SetBranchAddress("edep", &edep, &b_edep);
   fChain->SetBranchAddress("hitid", &hitid, &b_hitid);
   fChain->SetBranchAddress("track_list", &track_list_ptr, &b_track_list);
   fChain->SetBranchAddress("trackx", &trackx_ptr, &b_trackx);
   fChain->SetBranchAddress("tracky", &tracky_ptr, &b_tracky);
   fChain->SetBranchAddress("trackz", &trackz_ptr, &b_trackz);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   Notify();
}

Bool_t LxHitsTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}



// LxHittracks 
/////////////////////////////////////////////////////////////////////////
LxHittracks::LxHittracks(): eventid(-1), trackid(0), vtxx(0), vtxy(0), vtxz(0),
px(0), py(0), pz(0), E(0), pdg(0), pproc(0), ptid(0), weight(0)
{};

LxHittracks::LxHittracks(const LxHittracks &ht) :
eventid(ht.eventid), trackid(ht.trackid), vtxx(ht.vtxx), vtxy(ht.vtxy), vtxz(ht.vtxz),
px(ht.px), py(ht.py), pz(ht.pz), E(ht.E), pdg(ht.pdg), pproc(ht.pproc), ptid(ht.ptid), weight(ht.weight)
{}

LxHittracks::~LxHittracks()
{};



// LxHittracksTree
/////////////////////////////////////////////////////////////////////////
LxHittracksTree::LxHittracksTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
     throw std::invalid_argument("LxHittracksTree::LxHittracksTree TTree is null!");  
   }
   Init(tree);
}


LxHittracksTree::~LxHittracksTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t LxHittracksTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t LxHittracksTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void LxHittracksTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   trackid_ptr = &trackid;
   vtxx_ptr = &vtxx;
   vtxy_ptr = &vtxy;
   vtxz_ptr = &vtxz;
   px_ptr = &px;
   py_ptr = &py;
   pz_ptr = &pz;
   E_ptr = &E;
   pdg_ptr = &pdg;
   pproc_ptr = &pproc;
   ptid_ptr = &ptid;

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("eventid", &eventid, &b_eventid);
   fChain->SetBranchAddress("trackid", &trackid_ptr, &b_trackid);
   fChain->SetBranchAddress("vtxx", &vtxx_ptr, &b_vtxx);
   fChain->SetBranchAddress("vtxy", &vtxy_ptr, &b_vtxy);
   fChain->SetBranchAddress("vtxz", &vtxz_ptr, &b_vtxz);
   fChain->SetBranchAddress("px", &px_ptr, &b_px);
   fChain->SetBranchAddress("py", &py_ptr, &b_py);
   fChain->SetBranchAddress("pz", &pz_ptr, &b_pz);
   fChain->SetBranchAddress("E", &E_ptr, &b_E);
   fChain->SetBranchAddress("pdg", &pdg_ptr, &b_pdg);
   fChain->SetBranchAddress("pproc", &pproc_ptr, &b_pproc);
   fChain->SetBranchAddress("ptid", &ptid_ptr, &b_ptid);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   Notify();
}

Bool_t LxHittracksTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}



// LxTracks
/////////////////////////////////////////////////////////////////////////
LxTracks::LxTracks() : eventid(-1), trackid(0), detid(0), pdg(0), physproc(0), E(0),
x(0), y(0), z(0), t(0), vtxx(0), vtxy(0), vtxz(0), px(0), py(0), pz(0), theta(0), phi(0),
xlocal(0), ylocal(0), zlocal(0), weight(0), ptrackid(0), nsecondary(0)
{};

LxTracks::LxTracks(const LxTracks& tr): eventid(tr.eventid), trackid(tr.trackid), detid(tr.detid), 
pdg(tr.pdg), physproc(tr.physproc), E(tr.E), x(tr.x), y(tr.y), z(tr.z), t(tr.t), vtxx(tr.vtxx), 
vtxy(tr.vtxy), vtxz(tr.vtxz), px(tr.px), py(tr.py), pz(tr.pz), theta(tr.theta), phi(tr.phi),
xlocal(tr.xlocal), ylocal(tr.ylocal), zlocal(tr.zlocal), weight(tr.weight), 
ptrackid(tr.ptrackid), nsecondary(tr.nsecondary)
{};



LxTracks::~LxTracks()
{};



// LxTracksTree
/////////////////////////////////////////////////////////////////////////
LxTracksTree::LxTracksTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
     throw std::invalid_argument("LxTracksTree::LxTracksTree TTree is null!");  
   }
   Init(tree);
}


LxTracksTree::~LxTracksTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}


Int_t LxTracksTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}


Long64_t LxTracksTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void LxTracksTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   trackid_ptr = &trackid;
   detid_ptr = &detid;
   pdg_ptr = &pdg;
   physproc_ptr = &physproc;
   E_ptr = &E;
   x_ptr = &x;
   y_ptr = &y;
   z_ptr = &z;
   t_ptr = &t;
   vtxx_ptr = &vtxx;
   vtxy_ptr = &vtxy;
   vtxz_ptr = &vtxz;
   px_ptr = &px;
   py_ptr = &py;
   pz_ptr = &pz;
   theta_ptr = &theta;
   phi_ptr = &phi;
   xlocal_ptr = &xlocal;
   ylocal_ptr = &ylocal;
   zlocal_ptr = &zlocal;
   ptrackid_ptr = &ptrackid;
   nsecondary_ptr = &nsecondary;

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("eventid", &eventid, &b_eventid);
   fChain->SetBranchAddress("trackid", &trackid_ptr, &b_trackid);
   fChain->SetBranchAddress("detid", &detid_ptr, &b_detid);
   fChain->SetBranchAddress("pdg", &pdg_ptr, &b_pdg);
   fChain->SetBranchAddress("physproc", &physproc_ptr, &b_physproc);
   fChain->SetBranchAddress("E", &E_ptr, &b_E);
   fChain->SetBranchAddress("x", &x_ptr, &b_x);
   fChain->SetBranchAddress("y", &y_ptr, &b_y);
   fChain->SetBranchAddress("z", &z_ptr, &b_z);
   fChain->SetBranchAddress("t", &t_ptr, &b_t);
   fChain->SetBranchAddress("vtxx", &vtxx_ptr, &b_vtxx);
   fChain->SetBranchAddress("vtxy", &vtxy_ptr, &b_vtxy);
   fChain->SetBranchAddress("vtxz", &vtxz_ptr, &b_vtxz);
   fChain->SetBranchAddress("px", &px_ptr, &b_px);
   fChain->SetBranchAddress("py", &py_ptr, &b_py);
   fChain->SetBranchAddress("pz", &pz_ptr, &b_pz);
   fChain->SetBranchAddress("theta", &theta_ptr, &b_theta);
   fChain->SetBranchAddress("phi", &phi_ptr, &b_phi);
   fChain->SetBranchAddress("xlocal", &xlocal_ptr, &b_xlocal);
   fChain->SetBranchAddress("ylocal", &ylocal_ptr, &b_ylocal);
   fChain->SetBranchAddress("zlocal", &zlocal_ptr, &b_zlocal);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("ptrackid", &ptrackid_ptr, &b_ptrackid);
   fChain->SetBranchAddress("nsecondary", &nsecondary_ptr, &b_nsecondary);
   Notify();
}

Bool_t LxTracksTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}



//ProcessLxSim
/////////////////////////////////////////////////////////////////////////
ProcessLxSim::ProcessLxSim(const std::vector<std::string>  &flist)
{
  std::string hittreename("Hits");
  fHitChain = new TChain(hittreename.c_str());
  std::for_each(flist.begin(), flist.end(), [this](const std::string ss) {fHitChain->Add(ss.c_str());} );
  fHitTreeEntries = fHitChain->GetEntries();
  fHitTree = new LxHitsTree(fHitChain);
  fHitTreeEntry = 0;
  std::cout << "Hits entries: " << fHitTreeEntries << std::endl;

  std::string hittrcktreename("HitTracks");
  fHitTrackChain = new TChain(hittrcktreename.c_str());
  std::for_each(flist.begin(), flist.end(), [this](const std::string ss) {fHitTrackChain->Add(ss.c_str());} );
  fHitTrackTreeEntries = fHitTrackChain->GetEntries();
  fHitTrackTree = new LxHittracksTree(fHitTrackChain);
  fHitTrackTreeEntry = 0;
  std::cout << "HitTracks entries: " << fHitTrackTreeEntries << std::endl;
    
  std::string trcktreename("Tracks");
  fTrackChain = new TChain(trcktreename.c_str());
  std::for_each(flist.begin(), flist.end(), [this](const std::string ss) {fTrackChain->Add(ss.c_str());} );
  fTrackTreeEntries = fTrackChain->GetEntries();
  fTrackTree = new LxTracksTree(fTrackChain);
  fTrackTreeEntry = 0;
  fEventTrackId = -1;
  std::cout << "Tracks entries: " << fTrackTreeEntries << std::endl;
}



int ProcessLxSim::ReadNextEvent()
{
  int counthits, counthtracks;
  counthits = ReadNextHitEvent();
  counthtracks = ReadNextHitTrackEvent();
  // comment out by Arka
  if (fEventHitTrackId != fEventId) {
    std::cout << "Hits and HitTracks seem to be not synchronized!\n";
    return 0;
  }
  
  int counttrks;
  while(fEventTrackId != fEventId) {
    counttrks = ReadNextTrackEvent();
//     if (counttrks) continue;
//     std::cout << "Reading Tracks. Event: " <<  fEventTrackId << " Number of tracks: " << fTracks.size() << std::endl;
  }
  // comment out by Arka
  if (fEventHitTrackId != fEventId) {
    std::cout << "Hits and Tracks seem to be not synchronized!\n";
    return 0;
  }
  
  return counthits + counthtracks;
}



int ProcessLxSim::ReadNextHitTrackEvent()
{
  int ecount = 0;
  fHitTracks.clear();
  if (!fHitTrackTreeEntry) {
    if (!fHitTrackTree->GetEntry(fHitTrackTreeEntry)) return ecount;
  }
  if (fHitTrackTreeEntry >= fHitTrackTreeEntries) return ecount;
  fEventHitTrackId = fHitTrackTree->eventid;
  fHitTracks.push_back(LxHittracks(*fHitTrackTree));
  ecount += 1;
  while (fEventHitTrackId == fHitTrackTree->eventid && fHitTrackTreeEntry < fHitTrackTreeEntries) {
    if (!fHitTrackTree->GetEntry(++fHitTrackTreeEntry)) continue;
    if (fEventHitTrackId == fHitTrackTree->eventid) {
      fHitTracks.push_back(LxHittracks(*fHitTrackTree));
      ++ecount;
    }
  }
  return ecount;
}
  

  
int ProcessLxSim::ReadNextHitEvent()
{
  int ecount = 0;
  fHits.clear();
  if (!fHitTreeEntry) {
    if (!fHitTree->GetEntry(fHitTreeEntry)) return ecount;
  }
  if (fHitTreeEntry >= fHitTreeEntries) return ecount;
  fEventId = fHitTree->eventid;
  fHits.push_back(LxHits(*fHitTree));
  ecount += 1;
  while (fEventId == fHitTree->eventid && fHitTreeEntry < fHitTreeEntries) {
    if (!fHitTree->GetEntry(++fHitTreeEntry)) continue;
    if (fEventId == fHitTree->eventid) {
      fHits.push_back(LxHits(*fHitTree));
      ++ecount;
    }
  }
  return ecount;
}



int ProcessLxSim::ReadNextTrackEvent()
{
  int ecount = 0;
  fTracks.clear();
  if (!fTrackTreeEntry) {
    if (!fTrackTree->GetEntry(fTrackTreeEntry)) return ecount;
  }
  if (fTrackTreeEntry >= fTrackTreeEntries) return ecount;
  fEventTrackId = fTrackTree->eventid;
  fTracks.push_back(LxTracks(*fTrackTree));
  ecount += 1;
  while (fEventTrackId == fTrackTree->eventid && fTrackTreeEntry < fTrackTreeEntries) {
    if (!fTrackTree->GetEntry(++fTrackTreeEntry)) continue;
    if (fEventTrackId == fTrackTree->eventid) {
      fTracks.push_back(LxTracks(*fTrackTree));
      ++ecount;
    }
  }
  return ecount;
}


void ProcessLxSim::DumpEvent() const
{
  const auto &hitv = GetHits();
  const auto &hittrckv = GetHitTracks();
  std::cout << std::endl << "Event: " << fEventId << "  number oh hits: " << hitv.size() << std::endl;
  for (const auto &hit : hitv) {
    std::cout << "Event ID: " << hit.eventid << "  HitID: " << hit.hitid << "  DetID: " << hit.detid 
              << "      cell_x/cell_y/layer/edep: " << hit.cellx << "  " << hit.celly << "  " 
              << hit.layerid << "  " << hit.edep << std::endl;
    const auto &tridv = hit.track_list;
    const auto &trxv = hit.trackx;
    const auto &tryv = hit.tracky;
    const auto &trzv = hit.trackz;
    std::cout << "       Tracks ID: ";
    for (int ii : tridv) std::cout << ii << "  ";
    std::cout << std::endl;
    for (size_t ii = 0; ii < trxv.size(); ++ii) {
      std::cout << "  x/y/z: " << trxv.at(ii)
                << "  " << tryv.at(ii) << "  " << trzv.at(ii) << std::endl;
    }
  }

  std::cout << "Tracks event " << hittrckv[0].eventid << " : trackid / pdg / physproc / E / parent / "
            << "vtx_x / vtx_y / vtx_z\n";
  for (const auto &htrck : hittrckv) {
    for (size_t ii = 0; ii < htrck.trackid.size(); ++ii) {
      std::cout << std::setprecision(1)  << std::setw(10) << htrck.trackid.at(ii) 
                << std::setprecision(1)  << std::setw(10) << htrck.pdg.at(ii) 
                << std::setprecision(1)  << std::setw(10) << htrck.pproc.at(ii) 
                << std::setprecision(10) << std::setw(16) << htrck.E.at(ii) 
                << std::setprecision(1)  << std::setw(10) << htrck.ptid.at(ii) 
                << std::setprecision(10) << std::setw(16) << htrck.vtxx.at(ii)
                << std::setprecision(10) << std::setw(16) << htrck.vtxy.at(ii)
                << std::setprecision(10) << std::setw(16) << htrck.vtxz.at(ii) << std::endl;
    }
  }
}



