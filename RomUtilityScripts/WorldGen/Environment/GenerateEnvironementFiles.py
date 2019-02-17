from .DataImporter import ProceduralItemGroupSheetHandler, GrowableItemGroupSheetHandler


def generate_item_groups(outfile='Output/ItemGroups.sbc', handler=None):
    ss = ProceduralItemGroupSheetHandler() if not handler else handler
    ss.write_item_groups(ss.get_item_group_dict(), outfile)
    return outfile


def generate_growable_items(outfile='Output/GrowableEnvironmentItems.sbc', handler=None):
    ss = GrowableItemGroupSheetHandler() if not handler else handler
    ss.write_growable_items(ss.get_growable_items(), outfile)
    return outfile


def generate_tree_items(outfile='Output/TreeEnvironmentItems.sbc', handler=None):
    ss = GrowableItemGroupSheetHandler() if not handler else handler
    ss.write_growable_items(ss.get_growable_items('TreeEnvironmentItems'), outfile)
    return outfile


def generate_farmable_items(outfile='Output/FarmableEnvironmentItems.sbc', handler=None):
    ss = GrowableItemGroupSheetHandler() if not handler else handler
    ss.write_growable_items(ss.get_growable_items('FarmableEnvironmentItems', is_farmable=True), outfile)
    return outfile


def generate_environment_files():
    ss = GrowableItemGroupSheetHandler()
    out1 = generate_growable_items(handler=ss)
    out2 = generate_tree_items(handler=ss)
    out3 = generate_farmable_items(handler=ss)

    out4 = generate_item_groups()
    return out1, out2, out3, out4
