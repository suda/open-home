//
//  Device.m
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "Device.h"

@implementation Device

- (id)initWithPulseLength:(NSInteger)pulseLength onCode:(NSString *)onCode andOffCode:(NSString *)offCode {
    self = [super init];
    if (self) {
        _pulseLength = pulseLength;
        _triStateCodeOn = onCode;
        _triStateCodeOff = offCode;
    }
    
    return self;
}

- (NSDictionary *)toDictionary {
    NSMutableDictionary *dict =  [NSMutableDictionary new];
    
    [dict setObject:[NSNumber numberWithInteger:_pulseLength] forKey:@"pulseLength"];
    [dict setObject:_triStateCodeOn forKey:@"triStateCodeOn"];
    [dict setObject:_triStateCodeOff forKey:@"triStateCodeOff"];
    
    return dict;
}

- (NSString *)description {
    return [NSString stringWithFormat:@"Pulse length: %i, on code: %@, off code: %@", _pulseLength, _triStateCodeOn, _triStateCodeOff];
}

@end
