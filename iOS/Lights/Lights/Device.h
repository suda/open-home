//
//  Device.h
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Device : NSObject

- (id)initWithPulseLength:(NSInteger)pulseLength onCode:(NSString *)onCode andOffCode:(NSString *)offCode;

@property (nonatomic, assign) NSInteger pulseLength;
@property (nonatomic, retain) NSString *triStateCodeOn;
@property (nonatomic, retain) NSString *triStateCodeOff;

@end
