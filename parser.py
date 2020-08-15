import os
import json
import sys

# The region identity list structure:
# json::Array renderRegion(const coverage::CountedRegion &Region) {
#   return json::Array({Region.LineStart, Region.ColumnStart, Region.LineEnd,
#                       Region.ColumnEnd, int64_t(Region.ExecutionCount),
#                       Region.FileID, Region.ExpandedFileID,
#                       int64_t(Region.Kind)});
# }

def main():
    with open('libpng.json') as jsonfile:
        covered_regions = set()
        all_regions = set()
        
        coverage_info = json.load(jsonfile)
        functions_data = coverage_info['data'][0]['functions']
        
        # Index of the region identity list which indicates if it is hit.
        hit_index = 4
        # Index of the region identity list which indicates the type of the region.
        type_index = -1
        for function_data in functions_data:
            for region in function_data['regions']:
                region_identity = tuple(region[:hit_index]+region[5:]) # Skip the hit_index
                if (region[type_index] == 0): # 0 means it's code region 
                    all_regions.add(region_identity)
                if region[hit_index] != 0 and (region[type_index] == 0): # Code region that is covered
                    covered_regions.add(region_identity)
           

        coverage_data = coverage_info["data"][0]
        summary_data = coverage_data["totals"]
        regions_coverage_data = summary_data["regions"]
        expected_regions_covered = regions_coverage_data["covered"]
        expected_all_region = regions_coverage_data["count"] 
        print('expected covered: ', expected_regions_covered,
              'expected total region: ', expected_all_region) 
        
        print('counted covered: ', len(covered_regions), 
              'counted total region: ', len(all_regions))


if __name__ == '__main__':
    sys.exit(main())
