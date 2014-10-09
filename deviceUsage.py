

class Device:

   def __init__( self, name, watts ):
       self.name = name;
       self.watts = watts;
       self.kwatts = watts / 1000.0;
       self.computedWatts = -1;


class Devices:
    AllowableVariance = 0.1;

    def __init__( self ):
        self.deviceList = { };
        self.unknownDeviceList = [ ];
        return;

    def addDevice( self, name, watts ):
        device = Device( name, watts );
        self.deviceList[ name ] = device;
        return;

    def analyzeDetected( self, dset ):

        ##
        # associate the detected/computed value with each device
        #

        for dval in dset:
            found = False;
            for device in self.deviceList:
                tenPercentPos = self.deviceList[ device ].kwatts * ( Devices.AllowableVariance + 1 );
                tenPercentNeg = self.deviceList[ device ].kwatts * ( 1 - Devices.AllowableVariance );
                if ( dval <= tenPercentPos and dval >= tenPercentNeg ):
                    self.deviceList[ device ].computedWatts = dval;
                    found = True;
                    break;
            if ( not found ):
                self.unknownDeviceList.append( dval );

    def printResults( self ):
        print "True Positives";
        for device in self.deviceList:                
            if ( self.deviceList[ device ].computedWatts >= 0 ):
                print( "    %s expected: %5.2f detected: %5.2f" % 
                       ( device, self.deviceList[ device ].kwatts, self.deviceList[ device ].computedWatts ));
        print "False Negative - known devices not detected";
        for device in self.deviceList:                
            if ( self.deviceList[ device ].computedWatts < 0 ):
                print( "    %s expected: %5.2f detected: -" % ( device, self.deviceList[ device ].kwatts ));
        print "False Positive - unknown devices detected";
        print( "    " + str( self.unknownDeviceList ));


dev = Devices( );
dev.addDevice( "fridge", 200 );
dev.addDevice( "car", 1500 );
dev.addDevice( "dryer", 5000 );
dev.analyzeDetected( [ 0.19, 1.46, 1.8, 1.12 ]);
dev.printResults( );
