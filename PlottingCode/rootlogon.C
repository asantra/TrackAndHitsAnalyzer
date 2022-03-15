#include "LuxeStyle.C"
void rootlogon()
{
  // Load LUXE style
  //gROOT->LoadMacro("LuxeStyle.C"); //No longer works for ROOT6
  SetLuxeStyle();
}
