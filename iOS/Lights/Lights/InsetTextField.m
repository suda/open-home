//
//  InsetTextField.m
//  Lights
//
//  Created by Wojtek Siudzinski on 25.11.2013.
//  Copyright (c) 2013 Appsome. All rights reserved.
//

#import "InsetTextField.h"

@implementation InsetTextField

// placeholder position
- (CGRect)textRectForBounds:(CGRect)bounds {
    return CGRectInset( bounds , 10 , 10 );
}

// text position
- (CGRect)editingRectForBounds:(CGRect)bounds {
    return CGRectInset( bounds , 10 , 10 );
}

- (void) drawPlaceholderInRect:(CGRect)rect {
    [[self placeholder] drawInRect:rect withAttributes:@{NSForegroundColorAttributeName: [[UIColor whiteColor] colorWithAlphaComponent:0.5]}];
}

@end
