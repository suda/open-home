//
//  AddDeviceViewController.h
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "InsetTextField.h"
#import "OpenHome.h"
#import "Device.h"

@interface AddDeviceViewController : UIViewController

- (IBAction)addMoreDevices:(id)sender;

@property (weak, nonatomic) IBOutlet InsetTextField *pulseLengthField1;
@property (weak, nonatomic) IBOutlet InsetTextField *triStateCodeField1;

@property (weak, nonatomic) IBOutlet InsetTextField *pulseLengthField2;
@property (weak, nonatomic) IBOutlet InsetTextField *triStateCodeField2;

@property (weak, nonatomic) IBOutlet UIButton *addMoreButton;
@end
