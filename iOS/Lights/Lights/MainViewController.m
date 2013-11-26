//
//  MainViewController.m
//  Lights
//
//  Created by Wojtek Siudzinski on 22.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "MainViewController.h"

@interface MainViewController ()

@end

@implementation MainViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)loadView {
    [super loadView];
    
    [self.gesturedTableView setEnabled:YES];
    [self.gesturedTableView setEdgeSlidingMargin:0];
    [self.gesturedTableView setEdgeMovingMargin:80];

    // Settings button
    self.navigationItem.leftBarButtonItem = [[UIBarButtonItem alloc] initWithImage:[UIImage imageNamed:@"settings.png"] style:UIBarButtonItemStyleBordered target:self action:@selector(showSettings)];
    [self.navigationItem.leftBarButtonItem setTintColor:[UIColor whiteColor]];
    [self.navigationItem.leftBarButtonItem setTitleTextAttributes:[NSDictionary dictionaryWithObjectsAndKeys: [UIColor whiteColor], NSForegroundColorAttributeName, nil] forState:UIControlStateNormal];
    

    
    // Add device
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithImage:[UIImage imageNamed:@"add.png"] style:UIBarButtonItemStyleBordered target:self action:@selector(showAddDevice)];
    [self.navigationItem.rightBarButtonItem setTintColor:[UIColor whiteColor]];
    [self.navigationItem.rightBarButtonItem setTitleTextAttributes:[NSDictionary dictionaryWithObjectsAndKeys: [UIColor whiteColor], NSForegroundColorAttributeName, nil] forState:UIControlStateNormal];
    
    // Load saved lights
    [OpenHome sharedOpenHome];
}

- (void)showSettings {
    [[RootViewController sharedRootViewController] showLeftPanelAnimated:YES];
}

- (void)showAddDevice {
    [[RootViewController sharedRootViewController] showRightPanelAnimated:YES];
}

#pragma mark UITableView

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

-(NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return [[OpenHome sharedOpenHome].lights count];
}

-(PDGesturedTableViewCell *)tableView:(PDGesturedTableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *CellIdentifier = @"Cell";
    
    PDGesturedTableViewCell *cell = (PDGesturedTableViewCell *)[tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    if ([cell setupForGesturedTableView:tableView]) {
        [cell setBouncesAtLastSlidingFraction:YES];
        
        // Turn on gesture
        PDGesturedTableViewCellSlidingFraction *greenSlidingFraction = [PDGesturedTableViewCellSlidingFraction slidingFractionWithIcon:[UIImage imageNamed:@"off.png"] color:[UIColor colorWithRed:0.616 green:0.886 blue:0.733 alpha:1.000] activationFraction:0.01];
        [greenSlidingFraction setDidReleaseBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            [gesturedTableView replaceCell:cell completion:nil];
        }];
        [cell addSlidingFraction:greenSlidingFraction];
        
        PDGesturedTableViewCellSlidingFraction *onSlidingFraction = [PDGesturedTableViewCellSlidingFraction slidingFractionWithIcon:[UIImage imageNamed:@"on.png"] color:[UIColor colorWithRed:0.341 green:0.863 blue:0.565 alpha:1.000] activationFraction:0.25];
        
        [onSlidingFraction setDidActivateBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            turnOn = YES;
        }];
        
        [onSlidingFraction setDidDeactivateBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            turnOn = NO;
        }];
        
        [onSlidingFraction setDidReleaseBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            if (turnOn) {
                // TODO: Implement turning on
                NSLog(@"Turn ON");
                turnOn = NO;
            }
            [gesturedTableView replaceCell:cell completion:nil];
        }];
    
        [cell addSlidingFraction:onSlidingFraction];
        
        // Turn off gesture
        PDGesturedTableViewCellSlidingFraction *redSlidingFraction = [PDGesturedTableViewCellSlidingFraction slidingFractionWithIcon:[UIImage imageNamed:@"on.png"] color:[UIColor colorWithRed:1.000 green:0.729 blue:0.651 alpha:1.000] activationFraction:-0.01];
        [redSlidingFraction setDidReleaseBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            [gesturedTableView replaceCell:cell completion:nil];
        }];
        [cell addSlidingFraction:redSlidingFraction];
        
        PDGesturedTableViewCellSlidingFraction *offSlidingFraction = [PDGesturedTableViewCellSlidingFraction slidingFractionWithIcon:[UIImage imageNamed:@"off.png"] color:[UIColor colorWithRed:1.000 green:0.494 blue:0.353 alpha:1.000] activationFraction:-0.25];
        
        [offSlidingFraction setDidActivateBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            turnOff = YES;
        }];
        
        [offSlidingFraction setDidDeactivateBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            turnOff = NO;
        }];
        
        [offSlidingFraction setDidReleaseBlock:^(PDGesturedTableView * gesturedTableView, PDGesturedTableViewCell * cell) {
            if (turnOff) {
                // TODO: Implement turning off
                turnOff = NO;
                NSLog(@"Turn OFF");
            }
            [gesturedTableView replaceCell:cell completion:nil];
        }];
        
        [cell addSlidingFraction:offSlidingFraction];
    }

    return cell;
}

@end
