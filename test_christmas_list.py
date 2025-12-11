import os
import pickle
import pytest
from christmas_list import ChristmasList

@pytest.fixture
def filename():
    return "christmas_list.pkl"

@pytest.fixture
def filename_copy():
    return "christmas_list_copy.pkl"

@pytest.fixture
def nonempty_db(filename_copy):
    items = [
        {"name": "TestItemTrue", "purchased": True},
        {"name": "TestItemFalse", "purchased": False}
    ]
    with open(filename_copy, "wb") as f:
        pickle.dump(items, f)
    
@pytest.fixture(autouse=True)
def clone(filename_copy, filename):
    if os.path.exists(filename):
        with open(filename, "rb") as t:
            open(filename_copy, "wb").write(t.read())
    else:
        open(filename_copy, "wb").write(b"")
    yield

    if os.path.exists(filename_copy):
        os.remove(filename_copy)
        

def describe_christmas_list():
    def describe_init():
        def it_sets_the_filename_when_initializing(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            assert christmaslist.fname == filename_copy
        
        def it_creates_file_if_not_exists(filename_copy):
            if os.path.exists(filename_copy):
                os.remove(filename_copy)
            christmaslist = ChristmasList(filename_copy)
            assert os.path.isfile(filename_copy)
    
    def describe_add():
        def it_adds_item_to_empty_db(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.add("NewItem")
            items = christmaslist.loadItems()
            assert any(item["name"] == "NewItem" and item["purchased"] is False for item in items)
        
        def it_adds_multiple_items_to_list(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.add("Item1")
            christmaslist.add("Item2")
            christmaslist.add("Item3")
            items = christmaslist.loadItems()
            assert any(item["name"] == "Item1" for item in items)
            assert any(item["name"] == "Item2" for item in items)
            assert any(item["name"] == "Item3" for item in items)
        
        def it_adds_duplicate_names(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.add("duplicate")
            christmaslist.add("duplicate")
            items = christmaslist.loadItems()
            assert len(items) == 2
        
        def it_handles_empty_string_name(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.add("")
            items = christmaslist.loadItems()
            assert any(item["name"] == "" and item["purchased"] is False for item in items)
        
        def it_treats_names_as_case_sensitive(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.add("item")
            christmaslist.add("Item")
            christmaslist.add("ITEM")
            items = christmaslist.loadItems()
            assert len(items) == 3

    def describe_check_off():
        def it_checks_off_item_in_nonempty_db(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.check_off("TestItemFalse")
            items = christmaslist.loadItems()
            assert any(item["name"] == "TestItemFalse" and item["purchased"] is True for item in items)
            christmaslist.check_off("TestItemTrue")
            items = christmaslist.loadItems()
            assert any(item["name"] == "TestItemTrue" and item["purchased"] is True for item in items)
        
        def it_does_not_error_when_checking_off_nonexistent_item(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.check_off("NonexistentItem")  
            items = christmaslist.loadItems()
            assert len(items) == 2 
        
        def it_keeps_item_checked_when_checked_twice(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.check_off("TestItemTrue")
            christmaslist.check_off("TestItemTrue")
            items = christmaslist.loadItems()
            item = next(i for i in items if i["name"] == "TestItemTrue")
            assert item["purchased"] is True
        
    

    def describe_remove():
        def it_removes_item_from_nonempty_db(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.remove("TestItemTrue")
            items = christmaslist.loadItems()
            assert all(item["name"] != "TestItemTrue" for item in items)
        
        def it_does_not_error_when_removing_nonexistent_item(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.remove("NonexistentItem")
            items = christmaslist.loadItems()
            assert len(items) == 2
        
        def it_removes_all_items_with_same_name(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            items = [
                {"name": "Duplicate", "purchased": False},
                {"name": "Duplicate", "purchased": True},
                {"name": "Other", "purchased": False}
            ]
            christmaslist.saveItems(items)
            christmaslist.remove("Duplicate")
            remaining = christmaslist.loadItems()
            assert len(remaining) == 1
            assert remaining[0]["name"] == "Other"
        
        def it_does_not_error_removing_from_empty_list(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.remove("Item")
            items = christmaslist.loadItems()
            assert len(items) == 0
    
    def describe_print_list():
        def it_prints_items_in_nonempty_db(capsys, filename_copy,nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.print_list()
            captured = capsys.readouterr()
            assert "[x] TestItemTrue" in captured.out
            assert "[_] TestItemFalse" in captured.out
        
        def it_prints_nothing_for_empty_list(capsys, filename_copy):
            christmaslist = ChristmasList(filename_copy)
            christmaslist.print_list()
            captured = capsys.readouterr()
            assert captured.out == ""
    
    def describe_loadItems():
        def it_loads_items_from_nonempty_db(filename_copy, nonempty_db):
            christmaslist = ChristmasList(filename_copy)
            items = christmaslist.loadItems()
            assert len(items) == 2
            assert any(item["name"] == "TestItemTrue" and item["purchased"] is True for item in items)
            assert any(item["name"] == "TestItemFalse" and item["purchased"] is False for item in items)
        
        def it_loads_empty_list_from_new_file(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            items = christmaslist.loadItems()
            assert items == []
            assert len(items) == 0
    
    def describe_saveItems():
        def it_saves_items_to_file(filename_copy):
            christmaslist = ChristmasList(filename_copy)
            test_items = [
                {"name": "SavedItem1", "purchased": False},
                {"name": "SavedItem2", "purchased": True}
            ]
            christmaslist.saveItems(test_items)
            with open(filename_copy, "rb") as f:
                loaded_items = pickle.load(f)
            assert loaded_items == test_items
    