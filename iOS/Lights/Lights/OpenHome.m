//
//  OpenHome.m
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "OpenHome.h"

@implementation OpenHome

+ (OpenHome *)sharedOpenHome {
    static dispatch_once_t pred;
    static OpenHome *shared = nil;
    
    dispatch_once(&pred, ^{
        shared = [[OpenHome alloc] init];
    });
    return shared;
}

#pragma mark Instance methods

- (id)init {
    self = [super init];
    if (self) {
        userDefaults = [NSUserDefaults standardUserDefaults];
        documentsDirectory = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject];
        fileManager = [NSFileManager defaultManager];
        
        _serverAddress = [userDefaults stringForKey:@"serverAddress"];
        
        _lights = [NSMutableArray new];
        [_lights addObject:@"Bedroom"];
        [_lights addObject:@"Kitchen"];
        [_lights addObject:@"Living Room"];
        [_lights addObject:@"Kids Room"];                
        [_lights addObject:@"Stairs"];
        [_lights addObject:@"Garage"];
        [_lights addObject:@"Porch"];
        
        NSString *lightsPlistPath = [documentsDirectory stringByAppendingPathComponent:@"lights.plist"];
        
        if ([fileManager fileExistsAtPath:lightsPlistPath]) {
            NSArray *plist = [NSArray arrayWithContentsOfFile:lightsPlistPath];
            _lights = [plist mutableCopy];
        }
    }
    return self;
}

- (void)setServerAddress:(NSString *)serverAddress {
    _serverAddress = serverAddress;
    [userDefaults setObject:_serverAddress forKey:@"serverAddress"];
    [userDefaults synchronize];
}

- (void)addDeviceGroup:(NSArray *)group {
    [_lights addObject:group];
    
}

@end
