//
//  SettingsViewController.m
//  Lights
//
//  Created by Wojtek Siudzinski on 26.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "SettingsViewController.h"
#import "RootViewController.h"

@interface SettingsViewController ()

@end

@implementation SettingsViewController

- (void)viewWillAppear:(BOOL)animated {
    [_serverField setText:[OpenHome sharedOpenHome].serverAddress];
}

- (void)textFieldDidEndEditing:(UITextField *)textField {
    [[OpenHome sharedOpenHome] setServerAddress:_serverField.text];
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    [_serverField resignFirstResponder];
    [[RootViewController sharedRootViewController] toggleLeftPanel:nil];

    return YES;
}

@end
