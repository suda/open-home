//
//  AddDeviceViewController.m
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "AddDeviceViewController.h"
#import "RootViewController.h"

@interface AddDeviceViewController ()

@end

@implementation AddDeviceViewController

- (void)resetLayout {
    [_pulseLengthField1 setText:@""];
    [_triStateCodeField1 setText:@""];
    [_pulseLengthField2 setText:@""];
    [_triStateCodeField2 setText:@""];
    
    [_pulseLengthField2 setHidden:YES];
    [_triStateCodeField2 setHidden:YES];
    
    [_addMoreButton setHidden:NO];
    
    [_triStateCodeField1 setReturnKeyType:UIReturnKeyDone];
}

- (void)viewWillAppear:(BOOL)animated {
    [self resetLayout];
}

- (void)addDevices {
    NSString *device1Code = _triStateCodeField1.text;
    Device *device1 = [[Device alloc] initWithPulseLength:[_pulseLengthField1.text integerValue]
                                                   onCode:[device1Code stringByReplacingCharactersInRange:NSMakeRange(10, 2) withString:@"01"]
                                               andOffCode:[device1Code stringByReplacingCharactersInRange:NSMakeRange(10, 2) withString:@"10"]];
    
    if (_triStateCodeField2.isHidden) {
        [[OpenHome sharedOpenHome] addDeviceGroup:@[
            device1
        ]];
    } else {
        NSString *device2Code = _triStateCodeField2.text;
        Device *device2 = [[Device alloc] initWithPulseLength:[_pulseLengthField2.text integerValue]
                                                       onCode:[device2Code stringByReplacingCharactersInRange:NSMakeRange(10, 2) withString:@"01"]
                                                   andOffCode:[device2Code stringByReplacingCharactersInRange:NSMakeRange(10, 2) withString:@"10"]];
        
        [[OpenHome sharedOpenHome] addDeviceGroup:@[
            device1,
            device2
        ]];
    }
    
    [[RootViewController sharedRootViewController] toggleRightPanel:nil];
}

- (IBAction)addMoreDevices:(id)sender {
    [_addMoreButton setHidden:YES];
    
    [_pulseLengthField2 setHidden:NO];
    [_triStateCodeField2 setHidden:NO];
    
    [_triStateCodeField1 setReturnKeyType:UIReturnKeyNext];
}

#pragma mark - UITextFieldDelegate

- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    if (((textField.tag == 2) && _triStateCodeField2.isHidden) ||
        ((textField.tag == 4) && !_triStateCodeField2.isHidden)) {
        // Done
        
        if (((_triStateCodeField1.text.length == 12) && _triStateCodeField2.isHidden) ||
            ((_triStateCodeField1.text.length == 12) && (_triStateCodeField2.text.length == 12) && !_triStateCodeField2.isHidden)) {
            [textField resignFirstResponder];
            [self addDevices];
        }
    } else if ((textField.tag == 2) && !_triStateCodeField2.isHidden) {
        // Next from triStateCodeField1 to pulseLengthField2
        [_pulseLengthField2 becomeFirstResponder];
    }
    
    return YES;
}

@end
