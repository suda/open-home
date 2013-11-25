//
//  MainViewController.h
//  Lights
//
//  Created by Wojtek Siudzinski on 22.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "PDGesturedTableView.h"
#import "RootViewController.h"

@interface MainViewController : UITableViewController <UITableViewDataSource> {
    BOOL turnOn;
    BOOL turnOff;
    
    NSString *serverAddress;
    NSMutableArray *lights;
    NSString *documentsDirectory;
    NSFileManager *fileManager;
}

@property (nonatomic, retain) IBOutlet PDGesturedTableView *gesturedTableView;

@end
