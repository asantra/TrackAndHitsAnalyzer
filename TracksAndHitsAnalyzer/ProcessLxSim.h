//

#ifndef ProcessLxSim_h
#define ProcessLxSim_h 1

#include <vector>

class TChain;
class TTree;
class TBranch;


// LxHits
class LxHits 
{
public :

   Int_t            eventid;
   Int_t            detid;
   Int_t            layerid;
   Int_t            cellx;
   Int_t            celly;
   Double_t         edep;
   Int_t            hitid;
   std::vector<int>     track_list;
   std::vector<double>  trackx;
   std::vector<double>  tracky;
   std::vector<double>  trackz;
   Double_t         weight;

   LxHits();
   LxHits(const LxHits &hit);
   virtual ~LxHits();
};



// LxHitsTree
class LxHitsTree: public LxHits
{
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   std::vector<int>     *track_list_ptr;
   std::vector<double>  *trackx_ptr;
   std::vector<double>  *tracky_ptr;
   std::vector<double>  *trackz_ptr;

   // List of branches
   TBranch        *b_eventid;   //!
   TBranch        *b_detid;   //!
   TBranch        *b_layerid;   //!
   TBranch        *b_cellx;   //!
   TBranch        *b_celly;   //!
   TBranch        *b_edep;   //!
   TBranch        *b_hitid;   //!
   TBranch        *b_track_list;   //!
   TBranch        *b_trackx;   //!
   TBranch        *b_tracky;   //!
   TBranch        *b_trackz;   //!
   TBranch        *b_weight;   //!

   LxHitsTree(TTree *tree=0);
   virtual ~LxHitsTree();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual Bool_t   Notify();
};



// LxHittracks
class LxHittracks 
{
public:
  LxHittracks();
  LxHittracks(const LxHittracks &ht);
  virtual ~LxHittracks();
  
   Int_t                 eventid;
   std::vector<int>      trackid;
   std::vector<double>   vtxx;
   std::vector<double>   vtxy;
   std::vector<double>   vtxz;
   std::vector<double>   px;
   std::vector<double>   py;
   std::vector<double>   pz;
   std::vector<double>   E;
   std::vector<int>      pdg;
   std::vector<int>      pproc;
   std::vector<int>      ptid;
   Double_t              weight;
};



// LxHittracksTree
class LxHittracksTree: public LxHittracks 
{
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   vector<int>     *trackid_ptr;
   vector<double>  *vtxx_ptr;
   vector<double>  *vtxy_ptr;
   vector<double>  *vtxz_ptr;
   vector<double>  *px_ptr;
   vector<double>  *py_ptr;
   vector<double>  *pz_ptr;
   vector<double>  *E_ptr;
   vector<int>     *pdg_ptr;
   vector<int>     *pproc_ptr;
   vector<int>     *ptid_ptr;

   // List of branches
   TBranch        *b_eventid;   //!
   TBranch        *b_trackid;   //!
   TBranch        *b_vtxx;   //!
   TBranch        *b_vtxy;   //!
   TBranch        *b_vtxz;   //!
   TBranch        *b_px;   //!
   TBranch        *b_py;   //!
   TBranch        *b_pz;   //!
   TBranch        *b_E;   //!
   TBranch        *b_pdg;   //!
   TBranch        *b_pproc;   //!
   TBranch        *b_ptid;   //!
   TBranch        *b_weight;   //!

   LxHittracksTree(TTree *tree=0);
   virtual ~LxHittracksTree();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual Bool_t   Notify();
};



// LxTracks
class LxTracks 
{
public:
   Int_t           eventid;
   vector<int>     trackid;
   vector<int>     detid;
   vector<int>     pdg;
   vector<int>     physproc;
   vector<double>  E;
   vector<double>  x;
   vector<double>  y;
   vector<double>  z;
   vector<double>  t;
   vector<double>  vtxx;
   vector<double>  vtxy;
   vector<double>  vtxz;
   vector<double>  px;
   vector<double>  py;
   vector<double>  pz;
   vector<double>  theta;
   vector<double>  phi;
   vector<double>  xlocal;
   vector<double>  ylocal;
   vector<double>  zlocal;
   Double_t        weight;
   vector<int>     ptrackid;
   vector<int>     nsecondary;
   
   LxTracks();
   LxTracks(const LxTracks& tr);
   virtual ~LxTracks();
};


// LxTracksTree
class LxTracksTree : public LxTracks
{
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   vector<int>     *trackid_ptr;
   vector<int>     *detid_ptr;
   vector<int>     *pdg_ptr;
   vector<int>     *physproc_ptr;
   vector<double>  *E_ptr;
   vector<double>  *x_ptr;
   vector<double>  *y_ptr;
   vector<double>  *z_ptr;
   vector<double>  *t_ptr;
   vector<double>  *vtxx_ptr;
   vector<double>  *vtxy_ptr;
   vector<double>  *vtxz_ptr;
   vector<double>  *px_ptr;
   vector<double>  *py_ptr;
   vector<double>  *pz_ptr;
   vector<double>  *theta_ptr;
   vector<double>  *phi_ptr;
   vector<double>  *xlocal_ptr;
   vector<double>  *ylocal_ptr;
   vector<double>  *zlocal_ptr;
   vector<int>     *ptrackid_ptr;
   vector<int>     *nsecondary_ptr;

   // List of branches
   TBranch        *b_eventid;   //!
   TBranch        *b_trackid;   //!
   TBranch        *b_detid;   //!
   TBranch        *b_pdg;   //!
   TBranch        *b_physproc;   //!
   TBranch        *b_E;   //!
   TBranch        *b_x;   //!
   TBranch        *b_y;   //!
   TBranch        *b_z;   //!
   TBranch        *b_t;   //!
   TBranch        *b_vtxx;   //!
   TBranch        *b_vtxy;   //!
   TBranch        *b_vtxz;   //!
   TBranch        *b_px;   //!
   TBranch        *b_py;   //!
   TBranch        *b_pz;   //!
   TBranch        *b_theta;   //!
   TBranch        *b_phi;   //!
   TBranch        *b_xlocal;   //!
   TBranch        *b_ylocal;   //!
   TBranch        *b_zlocal;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_ptrackid;   //!
   TBranch        *b_nsecondary;   //!

   LxTracksTree(TTree *tree=0);
   virtual ~LxTracksTree();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual Bool_t   Notify();
};



//ProcessLxSim
class ProcessLxSim
{
public:
  ProcessLxSim(const std::vector<std::string>  &flist);
  
  const std::vector<LxHits>& GetHits() const { return fHits; }
  const std::vector<LxHittracks>& GetHitTracks() const { return fHitTracks; }
  const std::vector<LxTracks>& GetTracks() const { return fTracks; }
  int ReadNextEvent();
  int ReadNextHitEvent();
  int ReadNextHitTrackEvent();
  int ReadNextTrackEvent();
  void DumpEvent() const;
  

protected:
  TChain       *fHitChain;
  LxHitsTree   *fHitTree;
  int           fHitTreeEntry;
  int           fHitTreeEntries;
  std::vector<LxHits> fHits;
  int fEventId;
  
  TChain           *fHitTrackChain;
  LxHittracksTree  *fHitTrackTree;
  int               fHitTrackTreeEntry;
  int               fHitTrackTreeEntries;
  std::vector<LxHittracks> fHitTracks;
  int fEventHitTrackId;
  
  TChain           *fTrackChain;
  LxTracksTree     *fTrackTree;
  int               fTrackTreeEntry;
  int               fTrackTreeEntries;
  std::vector<LxTracks> fTracks;
  int fEventTrackId;
};



#endif

