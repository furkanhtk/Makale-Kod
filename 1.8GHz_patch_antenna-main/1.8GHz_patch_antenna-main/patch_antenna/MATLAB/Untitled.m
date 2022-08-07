Warning: "C:\Users\EFE\Desktop\8th_Term\EED4106\Finite Dipole" selected using
the Last Working Folder preference could not be accessed.
Using "C:\Users\EFE\Documents\MATLAB" as the initial working folder instead. 
insetpatch = patchMicrostripInsetfed

insetpatch = 

  patchMicrostripInsetfed with properties:

               Length: 0.0300
                Width: 0.0290
               Height: 0.0013
            Substrate: [1×1 dielectric]
    PatchCenterOffset: [0 0]
           FeedOffset: [-0.0300 0]
       StripLineWidth: 1.0000e-03
          NotchLength: 0.0080
           NotchWidth: 0.0030
    GroundPlaneLength: 0.0600
     GroundPlaneWidth: 0.0600
                 Tilt: 0
             TiltAxis: [1 0 0]
                 Load: [1×1 lumpedElement]

patchMicrostripInsetfed.Length = 0.03937;
patchMicrostripInsetfed.Width = 0.050807;
patchMicrostripInsetfed.Heigth = 0.000035;
d = dielectric('FR4'); 'Substrate',d

ans =

    'Substrate'


d = 

  dielectric with properties:

           Name: 'FR4'
       EpsilonR: 4.8000
    LossTangent: 0.0260
      Thickness: 0.0060

For more materials see catalog
patchMicrostripInsetfed.Substrate = 0.000035;
patchMicrostripInsetfed.Substrate = d;
patchMicrostripInsetfed.NotchLength = 1.23;
patchMicrostripInsetfed.NotchWidth = 0.86;
