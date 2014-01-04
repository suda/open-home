//
//  OpenHome.h
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface OpenHome : NSObject {
    NSString *documentsDirectory;
    NSFileManager *fileManager;
    NSUserDefaults *userDefaults;
}

+ (OpenHome *)sharedOpenHome;

- (void)addDeviceGroup:(NSArray *)group;

@property (nonatomic, retain) NSString *serverAddress;
@property (nonatomic, retain) NSMutableArray *lights;

@end
