//
//  {{file_name}}.m
//
//  Created by JSON2Mantle on {{created_at}}.
//  Copyright (c) {{year}} {{author}}. All rights reserved.
//

#import "{{file_name}}.h"
#import <Mantle/Mantle.h>

@implementation {{file_name}}


+ (NSDictionary *)JSONKeyPathsByPropertyKey
{
    // modelProperty : json_field_name
    return @{
            {{property_alias}}
            };
}

@end
