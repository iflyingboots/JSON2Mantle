//
//  {{file_name}}.m
//
//  Created by JSON2Mantle on {{created_at}}.
//  Copyright (c) {{year}} {{author}}. All rights reserved.
//

#import <Mantle.h>
#import "{{file_name}}.h"

@implementation {{file_name}}


+ (NSDictionary *)JSONKeyPathsByPropertyKey
{
    // modelProperty : json_field_name
    return @{
            {{property_alias}}
            };
}

{{transformers}}

@end
