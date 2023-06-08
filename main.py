import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import sqlite3
import random

#Window.size = (350,600)
x = Window.size[0]
y = Window.size[1]

nazvoslovi = {"ný": 1, "ná": 1, "natý": 2, "natá": 2, "itý": 3, "itá": 3, "ičitý": 4, "ičitá": 4, "ečná": 5,
                  "ičná": 5, "ová": 6, "istá": 7, "ičelá": 8, "ičný": 5, "ečný": 5, "ový": 6, "istý": 7, "ičelý": 8}

prvky2 = {"Cnatý": "uhelnatý", "Snatý": "sirnatý", "Sičitý": "siřičitý", "Sový": "sírový", "Liný": "lithný",
              "Naný": "sodný", "Kný": "draselný", "Rbný": "rubidný", "Csný": "cessný",
              "Benatý": "berylnatý", "Mgnatý": "hořečnatý", "Canatý": "vápenatý", "Srnatý": "strontnatý",
              "Banatý": "barnatý", "Bitý": "boritý", "Alitý": "hlinitý", "Gaitý": "gallitý",
              "Initý": "inditý", "Tlitý": "thallitý", "Tlný": "thallný", "Cičitý": "uhličitý", "Nnatý": "dusnatý",
              "Ničitý": "dusičitý", "Clistý": "chloristý", "Cličitý": "chloričitý",
              "Britý": "bromitý", "Pečný": "fosforečný", "Pitý": "fosforitý", "Siičitý": "křemičitý",
              "Iičný": "jodičný", "Iistý": "jodistý", "Mnistý": "manganistý", "Mničitý": "manganičitý",
              "Seový": "selenový", "Seičitý": "seleničitý", "Fný": "fluorný", "Clný": "chlorný",
              "Sbičný": "antimoničný", "Clečný":"chlorečný",
              "Moový": "molybdenový", "Sničitý": "cíničitý", "Asičný": "arseničný", "Osový": "osmiový",
              "Nitý": "dusitý", "Znnatý": "zinečnatý", "Vnatý": "vanadnatý", "Aunatý": "zlatnatý", "Nný": "dusný",
              "Cuný": "měďný", "Ninatý": "nikelnatý", "Pdnatý": "palladnatý", "Agnatý": "stříbrnatý",
              "Npičitý": "neptuničitý", "Osičelý": "osmičelý", "Xeičelý": "xenoničelý", "Hsičelý": "hassičelý",
              "Iričelý": "iridičelý", "Tcistý": "technecistý", "Reistý": "rhenistý", "Wičitý": "wolframičitý",
              "Auitý": "zlatitý", "Ceičitý": "ceričitý", "Niitý": "niklitý", "Snnatý": "cínatý",
              "Uový": "uranový", "Wový": "wolframový", "Uičitý": "uraničitý", "Puičitý": "plutoničitý",
              "Pbičitý": "olovičitý", "Taičný": "tantaličný", "Cdnatý": "kademnatý", "Laitý": "lanthanitý",
              "Smitý": "samaritý", "Sbitý": "antimonitý", "Cuitý": "měditý", "Conatý": "kobaltnatý",
              "Cunatý": "měďnatý", "Feitý": "železitý", "Fenatý": "železnatý", "Agný":"stříbrný", "Pbnatý": "olovnatý"}
prvky = {"sirnatý": "S", "siřičitý": "S", "sírový": "S", "siřičitá": "S", "lithný": "Li",
             "sodný": "Na", "draselný": "K", "rubidný": "Rb", "cesný": "Cs", "berylnatý": "Be", "hořečnatý": "Mg",
             "vápenatý": "Ca", "strontnatý": "Sr", "barnatý": "Ba", "boritý": "B", "hlinitý": "Al", "gallitý": "Ga",
             "inditý": "In", "thallitý": "Tl", "thallný": "Tl", "uhelnatý": "C", "uhličitý": "C", "dusnatý": "N",
             "dusičitý": "N", "chloristý": "Cl", "chloričitý": "Cl", "bromitý": "Br", "fosforečný": "P",
             "fosforitý": "P",  "manganistý": "Mn",
             "manganičitý": "Mn", "křemičitý": "Si",
              "dusičný": "N",
             "bromný": "Br", "bromistý": "Br", "bromičný": "Br", "jodý": "I", "jodistý": "I", "jodičný": "I",
              "fluorný": "F", "chlorečný": "Cl",
                "chlorný": "Cl", "tellurový": "Te",  "olovnatý": "Pb",
            "chromový": "Cr", "měďný": "Cu", "stříbrný":"Ag", "niklitý": "Ni", "ruthenatý": "Ru", "rtuťnatý":"Hg", "kobaltnatý":"Co",
            "ceričitý":"Ce", "antimoničný":"Sb", "molybdenový":"Mo", "cíničitý":"Sn", "arseničný":"As", "osmiový":"Os",
            "dusitý":"N", "zinečnatý":"Zn", "vanadnatý":"V", "zlatnatý":"Au", "dusný":"N", "nikelnatý":"Ni", "palladnatý":"Pd", "stříbrnatý":"Ag", "neptuničitý":"Np", "osmičelý":"Os",
         "xenoničelý":"Xe", "hassičelý":"Hs", "iridičelý":"Ir", "technecistý":"Tc", "rhenistý":"Re", "wolframičitý":"W", "zlatitý":"Au","cínatý": "Sn", "uranový":"U", "wolframový":"W",
         "uraničitý":"U", "plutoničitý":"Pu", "olovičitý":"Pb", "tantaličný":"Ta", "kademnatý":"Cd", "lanthanitý":"La", "samaritý":"Sm", "antimonitý":"Sb", "měditý":"Cu", "kovbaltnatý":"Co",
         "měďnatý":"Cu", "železitý":"Fe", "železnatý":"Fe", "amonný": "NH4"}
seznam = {"oxid měďný" : "Cu2O", "oxid chlorný" : "Cl2O","oxid lithný" : "Li2O","oxid dusný" : "N2O","oxid draselný" : "K2O","oxid rubidný" :"Rb2O","oxid stříbrný" :"Ag2O",
"oxid thallný": "Tl2O","oxid sodný" :"Na2O","oxid cesný" :"Cs2O","oxid gallný" : "Ga2O","voda" : "H2O","oxid barnatý" : "BaO","oxid berylnatý" : "BeO",
"oxid kademnatý": "CdO","oxid vápenatý" :"CaO","oxid uhelnatý" : "CO","oxid kobaltnatý": "CoO","oxid měďnatý" :"CuO","oxid železnatý" :"FeO","oxid olovnatý" :"PbO",
"oxid hořečnatý" :"MgO","oxid rtuťnatý" :"HgO","oxid nikelnatý" :"NiO","oxid dusnatý" :"NO","oxid palladnatý" :"PdO","oxid stříbrnatý" :"AgO","oxid strontnatý" :"SrO",
"oxid sirnatý" :"SO","oxid cínatý":"SnO","oxid titanatý" :"TiO","oxid vanadnatý" :"VO","oxid zinečnatý" :"ZnO","Oxid zlatnatý" :"AuO","oxid osminatý" :"OsO",
"oxid ruthenatý" :"RuO","oxid hlinitý": "Al2O3","oxid antimonitý" :"Sb2O3","oxid arsenitý" :"As4O6","oxid bismutitý" :"Bi2O3","oxid boritý" :"B2O3","oxid chromitý": "Cr2O3",
"oxid dusitý" :"N2O3","oxid erbitý" :"Er2O3","oxid gadolinitý": "Gd2O3","oxid gallitý" :"Ga2O3","oxid holmitý": "Ho2O3","Oxid inditý" :"In2O3","oxid železitý" :"Fe2O3",
"oxid lanthanitý": "La2O3","oxid lutecitý" :"Lu2O3","oxid niklitý" :"Ni2O3","oxid fosforitý" :"P4O6","oxid promethitý": "Pm2O3","oxid rhoditý": "Rh2O3",
"oxid samaritý" :"Sm2O3","oxid skanditý" :"Sc2O3","oxid terbitý" :"Tb2O3","oxid thallitý" :"Tl2O3","oxid thulitý" :"Tm2O3","oxid titanitý" :"Ti2O3","oxid wolframitý" :"W2O3",
"oxid vanaditý" :"V2O3","oxid ytterbitý" :"Yb2O3","oxid yttritý" :"Y2O3","oxid měditý" :"Cu2O3","oxid zlatitý" :"Au2O3","oxid chloritý" :"Cl2O3","oxid americitý": "Am2O3",
"oxid ruthenitý" :"Ru2O3","oxid uhličitý" :"CO2","oxid ceričitý" :"CeO2","oxid chloričitý" :"ClO2","oxid chromičitý" :"CrO2","oxid dusičitý": "NO2","oxid germaničitý": "GeO2",
"oxid hafničitý" :"HfO2","oxid molybdeničitý": "MoO2","oxid neptuničitý" :"NpO2","oxid osmičitý" :"OsO2","oxid olovičitý": "PbO2","oxid plutoničitý": "PuO2",
"oxid protaktiničitý": "PaO2","oxid rutheničitý": "RuO2","oxid seleničitý":"SeO2","oxid křemičitý" :"SiO2","oxid siřičitý" :"SO2", "oxid telluričitý" :"TeO2",
"oxid thoričitý": "ThO2","oxid cíničitý" :"SnO2","oxid titaničitý": "TiO2","oxid wolframičitý": "WO2","oxid uraničitý" :"UO2","oxid vanadičitý": "VO2","oxid zirkoničitý" :"ZrO2",
"oxid antimoničný" :"Sb2O5","oxid arseničný": "As2O5","oxid dusičný" :"N2O5","oxid fosforečný" :"P4O10","oxid tantaličný" :"Ta2O5","oxid vanadičný" :"V2O5","oxid chlorečný" :"Cl2O5",
"oxid molybdenový" :"MoO3","oxid rheniový": "ReO3","oxid selenový" :"SeO3","oxid sírový" :"SO3","oxid tellurový": "TeO3","oxid wolframový": "WO3","oxid uranový" :"UO3",
"oxid xenonový" :"XeO3","oxid rutheniový": "RuO3","oxid osmiový": "OsO3","oxid chloristý" : "Cl2O7","oxid manganistý" : "Mn2O7","oxid rhenistý" : "Re2O7","oxid technecistý" : "Tc2O7",
"oxid germanistý" : "Ge2O7","oxid selenistý" : "Se2O7","oxid osmičelý" : "OsO4","oxid rutheničelý" : "RuO4","oxid xenoničelý" : "XeO4","oxid hassičelý" : "HsO4",
"oxid iridičelý" : "IrO4"}
seznam2= {"CuO":"oxid měďnatý","Cl2O":"oxid chlorný", "Li2O":"oxid lithný", "N2O":"oxid dusný", "K20":"oxid draselný",
          "Rb2O": "oxid rubidný", "Ag2O":"oxid stříbrný", "Tl2O":"oxid thallný", "Na2O":"oxid sodný", "Cs2O":"oxid cesný",
          "Ga2O":"oxid gallný", "H2O":"voda", "BaO":"oxid barnatý", "BeO":"oxid berylnatý", "CdO":"oxid kademnatý", "CaO":"oxid vápenatý", "CO":"oxid uhelnatý",
          "CoO":"oxid kobaltnatý", "Cu2O":"oxid měďný", "FeO":"oxid železnatý", "PbO":"oxid olovnatý", "MgO":"oxid hořečnatý", "HgO":"oxid rtuťnatý", "NiO":"oxid nikelnatý",
          "NO":"oxid dusnatý", "PdO":"oxid palladnatý", "AgO":"oxid stříbrný", "SrO":"oxid strontnatý", "SO":"oxid sirnatý", "SnO":"oxid cínatý", "TiO":"oxid titanatý",
          "VO":"oxid vanadnatý", "ZnO":"oxid zinečnatý", "AuO":"oxid zlatnatý", "OsO":"oxid osminatý", "RuO":"oxid ruthenatý", "Al2O3":"oxid hlinitý", "Sb2O3":"oxid antimonitý",
          "As4O6":"oxid arsenitý", "Bi2O3":"oxid bismunitý", "B2O3":"oxid boritý", "Cr2O3":"oxid chromitý", "N2O3":"oxid dusitý", "Er2O3":"oxid erbitý", "Gd2O3":"oxid gadolinitý",
          "Ga2O3":"oxid gallitý", "Ho2O3":"oxid holmitý", "In2O3":"oxid inditý", "Fe2O3":"oxid železitý", "La2O3":"oxid lanthanitý", "Lu2O3":"oxid lutecitý", "Ni2O3":"oxid niklitý",
          "P4O6":"oxid fosforitý", "Pm2O3":"oxid promethitý", "Rh2O3":"oxid rhoditý", "Sm2O3":"oxid samaritý", "Sc2O3":"oxid skanditý", "Tb2O3":"oxid terbitý", "Tl2O3":"oxid thallitý",
          "Tm2O3":"oxid thulitý", "Ti2O3":"oxid titanitý", "W2O3":"oxid wolframitý", "V2O3":"oxid vanaditý", "Yb2O3":"oxid ytterbitý", "Y2O3":"oxid yttritý", "Cu2O3":"oxid meďitý",
          "Au2O3":"oxid zlatitý", "Cl2O3":"oxid chloritý", "Am2O3":"oxid americitý", "Ru2O3":"oxid ruthenitý", "CO2":"oxid uhličitý", "CeO2":"oxid ceričitý", "ClO":"oxid chloričitý",
          "CrO2":"oxid chromičitý", "NO2":"oxid dusičitý", "GeO2":"oxid germaničitý", "HfO2":"oxid hafničitý", "MoO2":"oxid molybdeničitý", "NpO2":"oxid neptuničitý", "OsO2":"oxid osmičitý",
          "PbO2":"oxid olivičitý", "PuO2":"oxid plutoničitý", "PaO2":"oxid protaktiničitý", "RuO2":"oxid rutheničitý", "SeO2":"oxid seleničitý", "SiO2":"oxid křemičitý",
          "SO2":"oxid siřičitý", "TeO2":"oxid telluričitý", "ThO2":"oxid thoričitý", "SnO2":"oxid cíničitý", "TiO2":"oxid titaničitý", "WO2":"oxid wolfamičitý", "UO2":"oxid uraničitý",
          "VO2":"oxid vanadičitý", "ZrO2":"oxid zirkoničitý", "Sb2O5":"oxid antimoničný", "As2O5":"oxid arseničný", "N2O5":"oxid dusičný", "P4O10":"oxid fosforečný",
          "Ta2O5":"oxid tantaličný", "V2O5":"oxid vanadičný", "Cl2O5":"oxid clorečný", "MoO3":"oxid molybdenový", "ReO2":"oxid rheniový", "SeO3":"oxid selenový", "SO3":"oxid sírový",
          "TeO3":"oxid tellurový", "WO3":"oxid wolframový", "UO3":"oxid uranový", "XeO3":"oxid xenonový", "RuO3":"oxid rutheniový", "OsO3":"oxid osmiový", "Cl2O7":"oxid chloristý",
          "Mn2O7":"oxid manganistý", "Re2O7":"oxid rhenistý", "Tc2O7":"oxid technecistý", "Ge2O7":"oxid germanistý", "Se2O7":"oxid selenistý", "OsO4":"oxid osmičelý",
          "RuO4":"oxid rutheničelý", "IrO4":"oxid iridičelý"}
seznam_kys= {"H2CrO4" : "kyselina chromová","H2Cr2O7" : "kyselina dichromová","HMnO4" : "kyselina manganistá","H2MnO4" : "kyselina manganová",
"HTcO4" : "kyselina technecistá","H2TcO4    " : "kyselina technetová","HReO4" : "Kyselina rhenistá","H2ReO4" : "kyselina rhenová","HReO3" : "kyselina rheničná",
"H3ReO4" : "kyselina trihydrogenrheničná","H4Re2O7" : "kyselina tetrahydrogenrheničná","H2FeO4" : "kyselina železová","H2RuO4" : "kyselina rutheniová",
"HRuO4" : "kyselina ruthenistá","H2RuO5" : "kyselina rutheničelá","H6OsO6" : "kyselina osmiová","H4OsO6" : "kyselina tetrahydrogenosmičelá",
"H3BO3" : "kyselina trihydrogenboritá","(HBO2)n" : "kyselina metaboritá","H2CO3" : "kyselina uhličitá","H4SiO4" : "kyselina orthokřemičitá","H2SiO3" : "kyselina křemičitá",
"HOCN" : "kyselina isokyanatá","HNO3" : "kyselina dusičná","HNO4" : "kyselina peroxodusičná","H3NO4" : "kyselina trihydrogendusičná","HNO2" : "kyselina dusitá",
"HOONO" : "kyselina peroxodusitá","H2NO2" : "kyselina dusičnatá","H2N2O2" : "kyselina dusná","H3PO4" : "kyselina trihydrogenfosforečná","HPO3" : "kyselina fosforečná",
"H4P2O7" : "kyselina tetrahydrogenfosforečná","H3PO5" : "kyselina peroxofosforečná","H2PHO3" : "kyselina fosforitá","H2P2H2O5" : "kyselina difosforitá",
"HPH2O2" : "kyselina fosforná","H3AsO4" : "kyselina trihydrogenarseničná","H3AsO3" : "kyselina trihydrogenarsenitá","H2SO4" : "kyselina sírová",
"H2S2O7" : "kyselina disírová","H2SO5" : "kyselina peroxosírová","H2S2O8" : "kyselina peroxodisírová","H2S2O6" : "kyselina dithionová","H2SO3" : "kyselina siřičitá",
"H2S2O5" : "kyselina tetrasírová","H2S2O3" : "kyselina thiosírová","H2S2O4" : "kyselina dithioničitá","H2S2O2" : "kyselina thiosiřičitá","H2SO2" : "kyselina sulfoxylová",
"HSOH" : "oxasulfan","H2SeO4" : "kyselina selenová","H2SeO3" : "kyselina seleničitá","H2TeO4" : "kyselina tellurová","H6TeO6" : "Kyselina hexahydrogentellurová",
"H2TeO3" : "kyselina telluričitá","HClO4" : "kyselina chloristá","HClO3" : "kyselina chlorečná","HClO2" : "kyselina chloritá","HClO" : "kyselina chlorná",
"HBrO4" : "kyselina bromistá", "HBrO3" : "kyselina bromičná","HBrO2" : "kyselina bromitá","HBrO" : "kyselina bromná","HIO4" : "kyselina jodistá",
"H5IO6" : "kyselina pentahydrogenjodistá","HIO3" : "kyselina jodičná","HIO" : "kyselina jodná","H2XeO4" : "Kyselina xenonová","H4XeO6" : "kyselina tetrahydrogenxenoničelá",
"HCN":"kyselina kyanovodíková","HN3":"kyselina azidovodíková", "H2S":"kyselina sirovodíková", "H2Se":"kyselina selenovodíková", "H2Te":"kyselina tellurovodíková",
"H2Po":"kyselina polanová", "HF":"kyselina fluorovodíková", "HCl":"kyselina chlorovodíková","HBr":"kyselina bromovodíková", "HI":"kyselina jodovodíková", "HAt":"kyselina astatovodíková",
"H3PO2S2":"kyselina trihydrogendithiofosforečná","HSCN":"kyselina thiokyanatá", "H2CS3":"kyselina trithiouhličitá", "H2SnS3":"kyselina trithiocíničitá", "H2COS2":"kyselina dithiouhličitá",
"H2S6O6":"kyselina hexathionová", "H3AsS4":"kyselina tetrathioarseničná", "H2MoO2S2":"kyselina dithiomolybdenová"

}
seznam_kys2 = {"kyselina tetrathioarseničná":"H3AsS4","kyselina dithiomolybdenová":"H2MoO2S2","kyselina hexathionová":"H2S6O6","kyselina trithiouhličitá":"H2CS3","kyselina thiokyanatá":"HSCN","kyselina trihydrogendithiofosforečná":"H3PO2S2", "kyselina dithiouhličitá":"H2COS2","kyselina trithiocíničitá":"H2SnS3","kyselina chromová":"H2CrO4", "kyselina dichromová": "H2Cr2O7", "kyselina manganistá":"HMnO4", "kyselina mangová":"H2MnO4", "kyselina technecistá": "HTcO4",
               "kyselina technetová":"H2TcO4", "kyselina rhenistá":"HReO4", "kyselina rhenová":"H2ReO4", "kyselina rheničná":"HReO3", "kyselina trihydrogenrheničná":"H3ReO4",
"kyselina tetrahydrogenrheničná":"H4Re2O7", "kyselina železová":"H2FeO4", "kyselina rutheniová":"H2RuO4", "kyselina ruthenistá":"HRuO4", "kyselina rutheničelá":"H2RuO5", 
"kyselina osmiová":"H6OsO6", "kyselina tetrahydrogenosmičelá":"H4OsO6", "kyselina trihydrogenbritá":"H3BO3", "kyselina metaboritá":"(HBO2)n", "kyselina uhličitá":"H2CO3", 
"kyselina orthokřemičitá":"H4SiO4", "kyselina křemičitá":"H2SiO3", "kyselina isokyanatá":"HOCN", "kyselina dusičná":"HNO3", "kyselina peroxodusičná":"HNO4",
               "kyselina trihydrogendusičná":"H3NO4", "kyselina dusitá":"HNO2", "kyselina peroxodusitá":"HOONO", "kyselina dusičnatá":"H2NO2", "kyselina dusná":"H2N2O2",
               "kyselina trihydrogenfosforečná":"H3PO4", "kyselina fosforečná":"HPO3", "kyselina tetrahydrogenfosforečná":"H4P2O7", "kyselina peroxofosforečná":"H3PO5",
               "kyselina fosforitá":"H3PO3", "kyselina difosforitá":"H2P2H2O5", "kyselina fosforná":"HPH2O2", "kyselina trihydrogenarseničná":"H3AsO4",
               "kyselina trihydrogenarsenitá":"H3AsO3", "kyselina sírová":"H2SO4", "kyslina disírová":"H2S2O7", "kyselina peroxosírová":"H2SO5", "kyselina peroxodisírová":"H2S2O8",
               "kyselina dithionová":"H2S2O6", "kyselina siřičitá":"H2SO3", "kyselina tetrasírová":"H2S2O5", "kyselina thiosírová":"H2S2O3", "kyselina dithioničitá":"H2S2O4",
               "kyselina thiosiřičitá":"H2S2O2", "kyselina sulfoxylová":"H2SO2", "oxasulfan":"HSOH", "kyselina selenová":"H2SeO4", "kyselina seleničitá":"H2SeO3",
               "kyselina tellurová":"H2TeO4", "kyselina hexahydrogentellurová":"H6TeO6", "kyselina telluričitá":"H2TeO3", "kyselina chloristá":"HClO4", "kyselina chlorečná":"HClO3",
               "kyselina chloritá":"HClO2", "kyselina chlorná":"HClO", "kyselina bromistá":"HBrO4", "kyselina bromičná":"HBrO3", "kyselina bromitá":"HBrO2", "kyselina bromná":"HBrO",
               "kyselina jodistá":"HIO4", "kyselina pentahydrogenjodistá":"H5IO6", "kyselina jodičná":"HIO3", "kyselina jodná":"HIO", "kyselina xenonová":"H2Xe4",
               "kyselina tetrahydrogenxenoničelá":"H4XeO6", "kyselina jodovodíková":"HI", "kyselina fluorovodíková":"HF", "kyselina bromovodíková":"HBr",
               "kyselina astatovodíková":"HAt", "kyselina sirovodíková":"H2S", "kyselina selenovodíková":"H2Se", "kyselina tellurovodíková":"H2Te", "kyselina polanová":"H2Po",
               "kyselina kyanovodíková":"HCN", "kyselina azidovodíková":"HN3", "kyselina chlorovodíková":"HCl"}
kys = {"fosforečnan": "(PO4)", "síran":"(SO4)", "siřičitan":"(SO3)", "křemičitan": "(SiO3)",
       "chlorečnan":"(ClO3)", "jodičnan": "(IO3)", "uhličitan":"(CO3)", "dusitan":"(NO2)",
       "chlornan":"(ClO)", "dusičnan":"(NO3)", "selenan":"(SeO4)", "arseničnan":"(AsO4)",
       "wolframan":"(WO4)", "boritan":"(BO2)", "bromičnan":"(BrO3)", "chloristan":"(ClO4)",
       "molybdenan":"(MoO4)", "tantaličnan":"(TaO3)", 
       "chroman":"(CrO4)","dichroman":"(Cr2O7)", "manganistan":"(MnO4)", "technecistan":"(TcO4)","rhenistan":"(ReO4)", "železan":"(FeO4)", "fosforitan":"(PO3)", "thiosíran":"(S2O3)", 
       "thiosiřičitan":"(S2O2)", "tetrasíran":"(S2O5)", "seleničitan":"(SeO3)", "chloritan":"(ClO2)", "bromistan":"(BrO4)" , "chlorid": "Cl", "fluorid":"F", "bromid":"Br", "jodid":"I",
       "sulfid":"S","kyanid":"CN"}
cisla_kys = {"(PO4)": 3, "(SO4)": 2,"(SO3)":2, "(SiO3)": 2, "(ClO3)": 1,"(IO3)":1,"(CO3)":2,
             "(NO2)": 1, "(ClO)": 1, "(NO3)":1, "(SeO4)":2 ,"(AsO4)":3, "(WO4)": 2,
             "(BO2)": 1, "(BrO3)": 1,"(ClO4)": 1, "(MoO4)": 2, "(TaO3)": 1, "(CrO4)":2, "(Cr2O7)":2, "(MnO4)":1, "(TcO4)":1,"(ReO4)":1, "(FeO4)":2, "(PO3)":3, "(S2O3)":2, "(S2O2)": 2,
             "(S2O5)": 2, "(SeO3)": 2, "(ClO2)":1, "(BrO4)":1}

#cesný

def nalezeni_cisla2(nazev):
    pole_cisel = []
    cislo = 0
    i = -1
    while i != -7:
        pole_cisel.append(nazev[i])
        pole1 = pole_cisel
        pole1.reverse()
        text_cisla = "".join(pole1)
        if text_cisla in nazvoslovi:
            cislo = nazvoslovi[text_cisla]
            i = i - 1
            text_cisla = ""
            pole1.reverse()

        else:
            i = i - 1
            text_cisla = ""
            pole1.reverse()
    return cislo

def nalezeni_cisla(nazev):
    cislo = 0
    for i in nazvoslovi:
        if i in nazev:
            cislo = nazvoslovi[i]
    return cislo
#N2(SO4)3 - dostaneme
#chlorid draselný
def soli_prvek(prvek):
    try:
        pole = []
        vysledek = []
        pole = prvek.split()
        prvni_prvek = pole[0]
        if pole[0] in kys:
            t1 = kys[pole[0]]
        else:
            return "nelze převést"
        if pole[1] in prvky:
            t2 = prvky[pole[1]]
        else:
            return "nelze převést"
        id = prvni_prvek[-2]+prvni_prvek[-1]
        if id != "id":
            oxid_cislo_kys = cisla_kys[t1]
            oxid_cislo_prvku = nalezeni_cisla(pole[1])
            if oxid_cislo_prvku == 0:
                return "neznámé oxidační číslo"
            if oxid_cislo_prvku %2 == 0 and oxid_cislo_kys % 2 == 0 or oxid_cislo_prvku == 6 and oxid_cislo_kys == 3 or oxid_cislo_prvku == oxid_cislo_kys:
                n_c1 = 1
                n_c2 = oxid_cislo_prvku/oxid_cislo_kys
            else:
                n_c1 = oxid_cislo_kys
                n_c2 = oxid_cislo_prvku
            vysledek.append(t2)
            if n_c1 > 1:
                vysledek.append(str(n_c1))

            vysledek.append(t1)
            if n_c2 > 1:
                vysledek.append(str(n_c2))
            vysledek1 = "".join(vysledek)
            return vysledek1
        elif id == "id":
            vysledek.append(t2)
            oxid_cislo_prvku = nalezeni_cisla(pole[1])
            if oxid_cislo_prvku == 0:
                return "neznámé oxidační číslo"
            if t1 == "S":
                if oxid_cislo_prvku%2 == 0:
                    vysledek.append(t1)
                    v_c = int(oxid_cislo_prvku/2)
                    if v_c != 1:
                        vysledek.append(str(v_c))
                    vysledek1 = "".join(vysledek)
                    return vysledek1
                else:
                    vysledek.append("2")
                    vysledek.append(t1)
                    if oxid_cislo_prvku != 1:
                        vysledek.append(str(oxid_cislo_prvku))
                    vysledek1 = "".join(vysledek)
                    return vysledek1
            else:
                vysledek.append(t1)
                if oxid_cislo_prvku != 1:
                    vysledek.append(str(oxid_cislo_prvku))
                vysledek1 = "".join(vysledek)
                return vysledek1
    except:
        return "nelze převést"

nazvoslovi2 = {1: "ný", 2: "natý", 3: "itý", 4: "ičitý", 5: "ečný", 6: "ový", 7: "istý", 8: "ičelý"}

def soli_nazev(nazev):
    try:
        vysledek = []
        if "(" in nazev and ")" in nazev:
            zavorka_1 = nazev.index("(")
            zavorka_2 = nazev.index(")")
            kyselina = nazev[zavorka_1:(zavorka_2 + 1)]
            if [k for k, v in kys.items() if v == kyselina]:
                nazev_kyseliny =[k for k, v in kys.items() if v == kyselina]
            else:
                return "nelze převést"
            nazev_kyseliny2 = "".join(nazev_kyseliny)
            vysledek.append(nazev_kyseliny2)
            cislo_kys = cisla_kys[kyselina]
            koncovka = nazev[-1]
            index = (nazev.index("("))-1
            if koncovka == ")":
                cislo = 1
            else:
                cislo = koncovka
            if int(cislo_kys) > 1 and int(cislo) > 1 and int(cislo)%2 == 0:
                final_cislo = int(cislo_kys)*int(cislo)
            elif int(cislo_kys) > 1 and int(cislo) == 1 and nazev[index] != 2:
                final_cislo = 2
            else:
                final_cislo = int(cislo)
            nazev_cisla = nazvoslovi2[int(final_cislo)]
            index_prvku = nazev[0:2]
            prvek = index_prvku + nazev_cisla
            if prvek in prvky2:
                nazev_prvku = prvky2[prvek]
                vysledek.append(nazev_prvku)
                vysledek1 = " ".join(vysledek)
                return vysledek1
            else:
                index_prvku = nazev[0]
                prvek = index_prvku + nazev_cisla
                if prvek in prvky2:
                    nazev_prvku = prvky2[prvek]
                    vysledek.append(nazev_prvku)
                    vysledek1 = " ".join(vysledek)
                    return vysledek1
                else:
                    return "nelze převést"
        else:
            end_letter = nazev[-1]
            if type(end_letter) == int:
                cislo = end_letter
            else:
                cislo = 1
            if "Cl" in nazev[1:]:
                nazev_kyseliny = "chlorid"
            elif "F" in nazev[1:]:
                nazev_kyseliny = "fluorid"
            elif "Br" in nazev[1:]:
                nazev_kyseliny = "bromid"
            elif "I" in nazev[1:]:
                nazev_kyseliny = "jodid"
            elif "CN" in nazev[1:]:
                nazev_kyseliny = "kyanid"
            elif "S" in nazev[1:]:
                nazev_kyseliny = "sulfid"
            else:
                return "nelze převést"
            prvek = nazev[0:2]
            if nazev_kyseliny == "sulfid":
                i = nazev.index("S")
                if nazev[i-1] != "2":
                    cislo = cislo*2
            cislo1 = nazvoslovi2[cislo]
            prvek_a_cislo = prvek+cislo1
            if prvek_a_cislo in prvky2:
                nazev_prvku = prvky2[prvek_a_cislo]
                vysledek.append(nazev_kyseliny)
                vysledek.append(nazev_prvku)
                vysledek1 = " ".join(vysledek)
                return vysledek1
            elif prvek_a_cislo not in prvky:
                prvek = nazev[0]
                cislo1 = nazvoslovi2[cislo]
                prvek_a_cislo = prvek + cislo1
                nazev_prvku = prvky2[prvek_a_cislo]
                vysledek.append(nazev_kyseliny)
                vysledek.append(nazev_prvku)
                vysledek1 = " ".join(vysledek)
                return vysledek1
            else:
                return "nelze převést"
    except:
        return "nelze převést"
def hydroxidy_nazvu(nazev):
    try:
        pole = []
        nazev = nazev.lower()
        prvek = nazev[9:]
        if prvek in prvky:
            pole.append(prvky[prvek])
        else:
            return "prvek nenalezen"
        pole.append("OH")
        cislo = nalezeni_cisla(nazev)
        if cislo == 0:
            return "neznámé oxidační číslo"
        if cislo > 1:
            pole.append(str(cislo))
        s = "".join(pole)
        return s
    except:
        return "chybné zadání"
def hydroxidy_vzorce(vzorec):
    try:
        pole2 = []
        pole = []
        pole.append("hydroxid")
        if vzorec[-1] == "H":
            cislo = 1
        else:
            cislo = vzorec[-1]
        nazev_cisla = nazvoslovi2[int(cislo)]
        index_prvku = vzorec[0:2]
        pole2.append(index_prvku)
        pole2.append(nazev_cisla)
        prvek = "".join(pole2)
        if prvek in prvky2:
            nazev_prvku = prvky2[prvek]
            pole.append(nazev_prvku)
            vysledek = " ".join(pole)
            return vysledek
        else:
            index_prvku = vzorec[0]
            prvek = index_prvku + nazev_cisla
            if prvek in prvky2:
                nazev_prvku = prvky2[prvek]
                pole.append(nazev_prvku)
                vysledek = " ".join(pole)
                return vysledek
            else:
                return "prvek nenalezen"
    except:
        return "chybné zadání"

class SecondWindow(Screen):
    Window.clearcolor = (255 / 255, 255 / 255, 255 / 255, 1)
    pole = []
    def velikost(self):
        x = Window.width/15
        y = Window.height/28
        return x,y


    def vysledek(self):
        input_all = self.ids.input.text
        k = input_all.split()
        x = input_all
        if input_all == "":
            self.ids.input.text = ""
            return False
        elif input_all in seznam_kys2:
            self.ids.input.text = seznam_kys2[input_all]
        elif "hydroxid" in input_all:
            self.ids.input.text = hydroxidy_nazvu(input_all)
        elif input_all in seznam_kys:
            self.ids.input.text = seznam_kys[input_all]
        elif "OH" in input_all:
            self.ids.input.text = hydroxidy_vzorce(input_all)
        elif input_all in seznam:
            self.ids.input.text = seznam[input_all]
        elif input_all in seznam2:
            self.ids.input.text = seznam2[input_all]
        elif k[0] in kys:
            self.ids.input.text = soli_prvek(input_all)
        elif [i for i in kys.values() if i in input_all]:
            self.ids.input.text = soli_nazev(input_all)
        else:
            self.ids.input.text = "nelze převést"
            #[i for i in kys.values() if i in input_all]
# elif "(" in input_all:
#self.ids.input.text = soli_nazev(input_all)

    def vysledekprint(self, input):
        k = input.split()
        if input == " ":
            x = ""
            return x
        elif input in seznam:
            x = seznam[input]
            return x
        elif input in seznam_kys2:
            x = seznam_kys2[input]
            return x
        elif input in seznam2:
            x = seznam2[input]
            return x
        elif input in seznam_kys:
            x = seznam_kys[input]
            return x
        elif "hydroxid" in input:
            x = hydroxidy_nazvu(input)
            return x
        elif "OH" in input:
            x = hydroxidy_vzorce(input)
            return x
        elif k[0] in kys:
            x = soli_prvek(input)
            return x
        elif [i for i in kys.values() if i in input]:
            x = soli_nazev(input)
            return x
        else:
            x = ""
            return x
    def add_historywidget(self):
        input_of_vzorce = self.ids.input.text
        if input_of_vzorce == "":
            pass
        else:
            y = SecondWindow().vysledekprint(input_of_vzorce)
            if y == "":
                pass
            else:
                array = SecondWindow().pole
                if input_of_vzorce not in array and y not in array:
                    self.ids.historylayout.add_widget(Label(text= f"{y} -> {input_of_vzorce}", color=(0.1,0.1,0.1,1), font_size=self.size[1]/35))
                    array.append(input_of_vzorce)
                    array.append(y)
                else:
                    pass


    def clear(self):
        self.ids.input.text = ""

    #Window.clearcolor = (255 / 255, 255 / 255, 1/ 255, 1)
    def show_p(self):
        PopupWindow.show_popup(self)

class PopupWindow(Screen):
    def show_popup(self):
        if Window.width < Window.height:
            x = Window.width/3
            a = 0.6
            b = 0.7
        elif Window.height < Window.width:
            x = Window.height /3
            a = 0.6
            b = 0.5
        else:
            x = Window.height /3
            a = 0.6
            b = 0.6
        show = PopupWindow()
        popupwindow = Popup(title="",content = show, size_hint=(None, None),pos_hint= {"x":a,"y":b},size = (x,x), separator_color= (255/255,255/255,255/255,1), background_color= (255,255,255,1))
        popupwindow.open()

class OAplikaciWindow(Screen):
    def velikost(self):
        cislo = (Window.width/100)*3.2
        return cislo
    def velikost2(self):
        cislo = (Window.width/100)*6
        return cislo
    def velikost3(self):
        cislo = (Window.width / 100) * 3.5
        return cislo

class StudiumWindow(Screen):
    pass

class OxidyWindow(Screen):
    pass

class KyselinyWindow(Screen):
    pass
class OxidyLearnWindow(Screen):
    def velikost(self):
        x = Window.width/500
        y = Window.height/500
        return x,y
class OxidyPrikladyWindow(Screen):
    def clear(self):
        self.ids.o1.text = ""
        self.ids.o2.text = ""
        self.ids.o3.text = ""
        self.ids.o4.text = ""
        self.ids.o5.text = ""
        self.ids.o6.text = ""
        self.ids.o7.text = ""
        self.ids.o8.text = ""
    def vyber(self):
        k = random.choice(list(seznam.keys()))
        self.ids.o11.text = random.choice(list(seznam2.keys()))
        self.ids.o22.text = random.choice(list(seznam.keys()))
        self.ids.o33.text = random.choice(list(seznam2.keys()))
        self.ids.o44.text = random.choice(list(seznam.keys()))
        self.ids.o55.text = random.choice(list(seznam2.keys()))
        self.ids.o66.text = random.choice(list(seznam.keys()))
        self.ids.o77.text = random.choice(list(seznam2.keys()))

    def kontrola(self):
        pole = []
        pole2 = []
        pocet = 0
        if self.ids.o1.text == seznam2[self.ids.o11.text]:
            pole.append(-1)
        else:
            pole.append(1)

        if self.ids.o2.text == seznam[self.ids.o22.text]:
            pole.append(-1)
        else:
            pole.append(2)

        if self.ids.o3.text == seznam2[self.ids.o33.text]:
            pole.append(-1)
        else:
            pole.append(3)

        if self.ids.o4.text == seznam[self.ids.o44.text]:
            pole.append(-1)
        else:
            pole.append(4)

        if self.ids.o5.text == seznam2[self.ids.o55.text]:
            pole.append(-1)
        else:
            pole.append(5)

        if self.ids.o6.text == seznam[self.ids.o66.text]:
            pole.append(-1)
        else:
            pole.append(6)

        if self.ids.o7.text == seznam2[self.ids.o77.text]:
            pole.append(-1)
        else:
            pole.append(7)

        if 1 not in pole and 2 not in pole and 3 not in pole and 4 not in pole and 5 not in pole and 6 not in pole and 7 not in pole:
            self.ids.o8.text = "Vše správně"
        else:
            for i in pole:
                if i >= 1:
                    pole2.append(str(i))
                else:
                    pass

            x = ", ".join(pole2)
            self.ids.o8.text = f"Odpovědi číslo {x} jsou nesprávné"

class KyselinyPrikladyWindow(Screen):
    def clear(self):
        self.ids.k1.text = ""
        self.ids.k2.text = ""
        self.ids.k3.text = ""
        self.ids.k4.text = ""
        self.ids.k5.text = ""
        self.ids.k6.text = ""
        self.ids.k7.text = ""
        self.ids.k8.text = ""
    def vyber(self):
        k = random.choice(list(seznam.keys()))
        self.ids.k11.text = random.choice(list(seznam_kys.keys()))
        self.ids.k22.text = random.choice(list(seznam_kys2.keys()))
        self.ids.k33.text = random.choice(list(seznam_kys.keys()))
        self.ids.k44.text = random.choice(list(seznam_kys2.keys()))
        self.ids.k55.text = random.choice(list(seznam_kys.keys()))
        self.ids.k66.text = random.choice(list(seznam_kys2.keys()))
        self.ids.k77.text = random.choice(list(seznam_kys.keys()))

    def kontrola(self):
        pole = []
        pole2 = []
        pocet = 0
        if self.ids.k1.text == seznam_kys[self.ids.k11.text]:
            pole.append(-1)
        else:
            pole.append(1)
        if self.ids.k2.text == seznam_kys2[self.ids.k22.text]:
            pole.append(-1)
        else:
            pole.append(2)
        if self.ids.k3.text == seznam_kys[self.ids.k33.text]:
            pole.append(-1)
        else:
            pole.append(3)
        if self.ids.k4.text == seznam_kys2[self.ids.k44.text]:
            pole.append(-1)
        else:
            pole.append(4)
        if self.ids.k5.text == seznam_kys[self.ids.k55.text]:
            pole.append(-1)
        else:
            pole.append(5)
        if self.ids.k6.text == seznam_kys2[self.ids.k66.text]:
            pole.append(-1)
        else:
            pole.append(6)
        if self.ids.k7.text == seznam_kys[self.ids.k77.text]:
            pole.append(-1)
        else:
            pole.append(7)

        if 1 not in pole and 2 not in pole and 3 not in pole and 4 not in pole and 5 not in pole and 6 not in pole and 7 not in pole:
            self.ids.k8.text = "Vše správně"
        else:
            for i in pole:
                if i >= 1:
                    pole2.append(str(i))
                else:
                    pass

            x = ", ".join(pole2)
            self.ids.k8.text = f"Odpovědi číslo {x} jsou nesprávné"

class HydroxidyWindow(Screen):
    pass
class HydroxidyPrikladyWindow(Screen):
    def clear(self):
        self.ids.h1.text = ""
        self.ids.h2.text = ""
        self.ids.h3.text = ""
        self.ids.h4.text = ""
        self.ids.h5.text = ""
        self.ids.h6.text = ""
        self.ids.h7.text = ""
        self.ids.h8.text = ""
    def funkce(self):
        x = random.choice(list(prvky.keys()))
        value = prvky[x]
        cislo = nalezeni_cisla(x)
        return value, cislo
    def vyber(self):
        x,y = HydroxidyPrikladyWindow().funkce()
        if y != 1:
            self.ids.h11.text = f"{x}OH{y}"
        else:
            self.ids.h11.text = f"{x}OH"

        x, y = HydroxidyPrikladyWindow().funkce()
        if y != 1:
            self.ids.h33.text = f"{x}OH{y}"
        else:
            self.ids.h33.text = f"{x}OH"

        x, y = HydroxidyPrikladyWindow().funkce()
        if y != 1:
            self.ids.h55.text = f"{x}OH{y}"
        else:
            self.ids.h55.text = f"{x}OH"

        x, y = HydroxidyPrikladyWindow().funkce()
        if y != 1:
            self.ids.h77.text = f"{x}OH{y}"
        else:
            self.ids.h77.text = f"{x}OH"

        self.ids.h22.text = f"hydroxid {random.choice(list(prvky.keys()))}"
        self.ids.h44.text = f"hydroxid {random.choice(list(prvky.keys()))}"
        self.ids.h66.text = f"hydroxid {random.choice(list(prvky.keys()))}"
    def kontrola(self):
        pole = []
        pole2 = []
        pocet = 0
        if self.ids.h1.text == hydroxidy_vzorce(self.ids.h11.text):
            pole.append(-1)
        else:
            pole.append(1)
        if self.ids.h2.text == hydroxidy_nazvu(self.ids.h22.text):
            pole.append(-1)
        else:
            pole.append(2)
        if self.ids.h3.text == hydroxidy_vzorce(self.ids.h33.text):
            pole.append(-1)
        else:
            pole.append(3)
        if self.ids.h4.text == hydroxidy_nazvu(self.ids.h44.text):
            pole.append(-1)
        else:
            pole.append(4)
        if self.ids.h5.text == hydroxidy_vzorce(self.ids.h55.text):
            pole.append(-1)
        else:
            pole.append(5)
        if self.ids.h6.text == hydroxidy_nazvu(self.ids.h66.text):
            pole.append(-1)
        else:
            pole.append(6)
        if self.ids.h7.text == hydroxidy_vzorce(self.ids.h77.text):
            pole.append(-1)
        else:
            pole.append(7)

        if 1 not in pole and 2 not in pole and 3 not in pole and 4 not in pole and 5 not in pole and 6 not in pole and 7 not in pole:
            self.ids.h8.text = "Vše správně"
        else:
            for i in pole:
                if i >= 1:
                    pole2.append(str(i))
                else:
                    pass

            x = ", ".join(pole2)
            self.ids.h8.text = f"Odpovědi číslo {x} jsou nesprávné"
class HydroxidyLearnWindow(Screen):
    def velikost(self):
        x = Window.width / 500
        y = Window.height / 500
        return x, y
class KyselinyLearnWindow(Screen):
    def velikost(self):
        x = Window.width / 500
        y = Window.height / 500
        return x, y

class SoliWindow(Screen):
    pass

class SoliPrikladyWindow(Screen):
    def clear(self):
        self.ids.s1.text = ""
        self.ids.s2.text = ""
        self.ids.s3.text = ""
        self.ids.s4.text = ""
        self.ids.s5.text = ""
        self.ids.s6.text = ""
        self.ids.s7.text = ""
        self.ids.s8.text = ""
    def funkce(self):
        x = random.choice(list(prvky.keys()))
        value = prvky[x]
        cislo = nalezeni_cisla(x)
        return value, cislo
    def funkce2(self):
        x = random.choice(list(cisla_kys.keys()))
        y = cisla_kys[x]
        return x,y
    def vyber(self):
        x,oxid_cislo_prvku = SoliPrikladyWindow().funkce()
        a,oxid_cislo_kys = SoliPrikladyWindow().funkce2()
        if oxid_cislo_prvku % 2 == 0 and oxid_cislo_kys % 2 == 0 or oxid_cislo_prvku == 6 and oxid_cislo_kys == 3 or oxid_cislo_prvku == oxid_cislo_kys:
            n_c1 = 1
            n_c2 = int(oxid_cislo_prvku / oxid_cislo_kys)
        else:
            n_c1 = int(oxid_cislo_kys)
            n_c2 = int(oxid_cislo_prvku)
        if n_c1 == 1 and n_c2 != 1 and n_c2 != 0 or n_c1 == 0 and n_c2 != 1 and n_c2 != 0:
            self.ids.s11.text = f"{x}{a}{int(n_c2)}"
        elif n_c2 == 1 and n_c1 != 1 and n_c1 != 0 or n_c2 == 0 and n_c1 != 1 and n_c1 != 0:
        	self.ids.s11.text = f"{x}{int(n_c1)}{a}" 
        elif n_c1 == 0 and n_c2 == 0:
            self.ids.s11.text = f"{x}{a}"
        elif n_c1 == 1 and n_c2 == 1:
            self.ids.s11.text = f"{x}{a}"
        else:
            self.ids.s11.text = f"{x}{int(n_c1)}{a}{int(n_c2)}"

        self.ids.s22.text = f"{random.choice(list(kys.keys()))} {random.choice(list(prvky.keys()))}"

        x, oxid_cislo_prvku = SoliPrikladyWindow().funkce()
        a, oxid_cislo_kys = SoliPrikladyWindow().funkce2()
        if oxid_cislo_prvku % 2 == 0 and oxid_cislo_kys % 2 == 0 or oxid_cislo_prvku == 6 and oxid_cislo_kys == 3 or oxid_cislo_prvku == oxid_cislo_kys:
            n_c1 = 1
            n_c2 = int(oxid_cislo_prvku / oxid_cislo_kys)
        else:
            n_c1 = int(oxid_cislo_kys)
            n_c2 = int(oxid_cislo_prvku)
        if n_c1 == 1 and n_c2 != 1 and n_c2 != 0 or n_c1 == 0 and n_c2 != 1 and n_c2 != 0:
            self.ids.s33.text = f"{x}{a}{int(n_c2)}"
        elif n_c2 == 1 and n_c1 != 1 and n_c1 != 0 or n_c2 == 0 and n_c1 != 1 and n_c1 != 0:
        	self.ids.s33.text = f"{x}{int(n_c1)}{a}" 
        elif n_c1 == 0 and n_c2 == 0:
            self.ids.s33.text = f"{x}{a}"
        elif n_c1 == 1 and n_c2 == 1:
            self.ids.s33.text = f"{x}{a}" 
        else:
            self.ids.s33.text = f"{x}{int(n_c1)}{a}{int(n_c2)}"

        self.ids.s44.text = f"{random.choice(list(kys.keys()))} {random.choice(list(prvky.keys()))}"

        x, oxid_cislo_prvku = SoliPrikladyWindow().funkce()
        a, oxid_cislo_kys = SoliPrikladyWindow().funkce2()
        if oxid_cislo_prvku % 2 == 0 and oxid_cislo_kys % 2 == 0 or oxid_cislo_prvku == 6 and oxid_cislo_kys == 3 or oxid_cislo_prvku == oxid_cislo_kys:
            n_c1 = 1
            n_c2 = oxid_cislo_prvku / oxid_cislo_kys
        else:
            n_c1 = oxid_cislo_kys
            n_c2 = oxid_cislo_prvku
        if n_c1 == 1 and n_c2 != 1 and n_c2 != 0 or n_c1 == 0 and n_c2 != 1 and n_c2 != 0:
            self.ids.s55.text = f"{x}{a}{int(n_c2)}"
        elif n_c2 == 1 and n_c1 != 1 and n_c1 != 0 or n_c2 == 0 and n_c1 != 1 and n_c1 != 0:
        	self.ids.s55.text = f"{x}{int(n_c1)}{a}" 
        elif n_c1 == 0 and n_c2 == 0:
            self.ids.s55.text = f"{x}{a}"
        elif n_c1 == 1 and n_c2 == 1:
            self.ids.s55.text = f"{x}{a}"
        else:
            self.ids.s55.text = f"{x}{int(n_c1)}{a}{int(n_c2)}"

        self.ids.s66.text = f"{random.choice(list(kys.keys()))} {random.choice(list(prvky.keys()))}"

        x, oxid_cislo_prvku = SoliPrikladyWindow().funkce()
        a, oxid_cislo_kys = SoliPrikladyWindow().funkce2()
        if oxid_cislo_prvku % 2 == 0 and oxid_cislo_kys % 2 == 0 or oxid_cislo_prvku == 6 and oxid_cislo_kys == 3 or oxid_cislo_prvku == oxid_cislo_kys:
            n_c1 = 1
            n_c2 = int(oxid_cislo_prvku / oxid_cislo_kys)
        else:
            n_c1 = int(oxid_cislo_kys)
            n_c2 = int(oxid_cislo_prvku)
        if n_c1 == 1 and n_c2 != 1 and n_c2 != 0 or n_c1 == 0 and n_c2 != 1 and n_c2 != 0:
            self.ids.s77.text = f"{x}{a}{int(n_c2)}"
        elif n_c2 == 1 and n_c1 != 1 and n_c1 != 0 or n_c2 == 0 and n_c1 != 1 and n_c1 != 0:
        	self.ids.s77.text = f"{x}{int(n_c1)}{a}" 
        elif n_c1 == 0 and n_c2 == 0:
            self.ids.s77.text = f"{x}{a}"
        elif n_c1 == 1 and n_c2 == 1:
            self.ids.s77.text = f"{x}{a}"
        else:
            self.ids.s77.text = f"{x}{int(n_c1)}{a}{int(n_c2)}"

    def kontrola(self):
        pole = []
        pole2 = []
        pocet = 0
        if self.ids.s1.text == soli_nazev(self.ids.s11.text):
            pole.append(-1)
        else:
            pole.append(1)
        if self.ids.s2.text == soli_prvek(self.ids.s22.text):
            pole.append(-1)
        else:
            pole.append(2)
        if self.ids.s3.text == soli_nazev(self.ids.s33.text):
            pole.append(-1)
        else:
            pole.append(3)
        if self.ids.s4.text == soli_prvek(self.ids.s44.text):
            pole.append(-1)
        else:
            pole.append(4)
        if self.ids.s5.text == soli_nazev(self.ids.s55.text):
            pole.append(-1)
        else:
            pole.append(5)
        if self.ids.s6.text == soli_prvek(self.ids.s66.text):
            pole.append(-1)
        else:
            pole.append(6)
        if self.ids.s7.text == soli_nazev(self.ids.s77.text):
            pole.append(-1)
        else:
            pole.append(7)

        if 1 not in pole and 2 not in pole and 3 not in pole and 4 not in pole and 5 not in pole and 6 not in pole and 7 not in pole:
            self.ids.s8.text = "Vše správně"
        else:
            for i in pole:
                if i >= 1:
                    pole2.append(str(i))
                else:
                    pass

            x = ", ".join(pole2)
            self.ids.s8.text = f"Odpovědi číslo {x} jsou nesprávné"

class SoliLearnWindow(Screen):
    def velikost(self):
        x = Window.width / 500
        y = Window.height / 500
        return x, y


class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("chemtry.kv")

class ChemtryApp(App):
    def build(self):
        self.icon = "icon.png"
        return kv

if __name__ == "__main__":
    ChemtryApp().run()