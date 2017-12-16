""" Test Person
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""
import unittest

from arthur_person import Person, Gender, PersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('female'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('FEMALE'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(PersonError) as context:
            Gender().get_gender('---')
        self.assertIn('Illegal gender', str(context.exception))


class TestPerson(unittest.TestCase):

    def setUp(self):
        # create a few Persons
        self.child = Person('kid', 'NA')
        self.mom = Person('mom', 'f')
        self.dad = Person('dad', 'm')

        # make a deep family history
        
        self.generations = 4
        self.people = people = []
        self.root_child = Person('root_child', Gender.UNKNOWN)
        people.append(self.root_child)
        
        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = Person(child.name + '_dad', Gender.MALE)
                mom = Person(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)
        
    ## Tests both accurate info and PersonError
    def test_set_mother(self):
        self.child.set_mother(self.mom)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)
        self.mom.gender = Gender.MALE
        with self.assertRaises(PersonError) as context:
            self.child.set_mother(self.mom)
        self.assertIn('is not female', str(context.exception))
     

        
    ## Tests both accurate info and PersonError
    def test_set_father(self):
        self.child.set_father(self.dad)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)
        self.dad.gender = Gender.FEMALE
        with self.assertRaises(PersonError) as context:
            self.child.set_father(self.dad)
        self.assertIn('is not male', str(context.exception))
    
    
    def test_add_child(self):
        self.assertNotIn(self.child, self.mom.children)
        self.mom.add_child(self.child)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)
        self.assertNotIn(self.child, self.dad.children)
        self.dad.add_child(self.child)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)
    
    def test_add_child_error(self):
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        ## Changed in other code to account for string specificity 
        self.assertIn('cannot add child', str(context.exception))
        self.assertIn('with unknown gender', str(context.exception))
        ##New test here for already has mom (same test could be run for dad)
        self.mom.add_child(self.child)
        with self.assertRaises(PersonError) as context:
            self.mom.add_child(self.child)
        self.assertIn("already has a mother", str(context.exception))

    
    def test_remove_mother(self):
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        self.assertNotIn(self.child, self.mom.children)
        
    ## Tests the PersonErrors Raised in Code
    def test_remove_mother_error(self):
        ## Tests if mother is none
        self.child.mother = None
        with self.assertRaises(PersonError) as context:
            self.child.remove_mother()
        self.assertIn('does not have a set mother', str(context.exception))
        
        
    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)
        
 
    def test_remove_father_error(self):
        self.child.father = None
        with self.assertRaises(PersonError) as context:
            self.child.remove_father()
        self.assertIn('does not have a set father', str(context.exception))
    
    def test_get_persons_name(self):
        self.assertEqual(Person.get_persons_name(self.dad), 'dad')
        self.assertEqual(Person.get_persons_name(None), 'NA')
        self.assertEqual(Person.get_persons_name(self.child), self.child.name)
        

    def test_grandparents(self):
        ## First find list of granparents names
        ## Sort to maintain order (switched from sort to set after class discussion)
        ## Test grandparents 4 (added after class discussion)
        g_parents = set([Person.get_persons_name(i) for i in self.root_child.grandparents()])
        #print(g_parents)
        real_gparents = set(['root_child_dad_mom', 'root_child_mom_dad', 'root_child_dad_dad', 'root_child_mom_mom'])
        self.assertEqual(g_parents, real_gparents)
        self.assertEqual(len(g_parents), 4)
        
    def test_grandparents_error(self):
        g_parents = set([Person.get_persons_name(i) for i in self.root_child.grandparents()])
        real_b_gparents = set(['root_child_dad_mum', 'root_child_mom_dad', 'root_child_da_dad', 'root_child_mom_mom'])
        self.assertNotEqual(g_parents, real_b_gparents)

        
    def test_all_granparents(self):
        ## First find list of grandparents names
        allg_parents = set([Person.get_persons_name(i) for i in self.root_child.all_grandparents()])
        #print(allg_parents)
        #print(len(allg_parents))
        real_allgparents = set(['root_child_mom_mom_mom', 'root_child_dad_dad_mom', 'root_child_mom_dad_mom', 'root_child_dad_dad_dad', 'root_child_mom_dad_dad', 'root_child_mom_mom_dad', 'root_child_mom_dad', 'root_child_mom_mom', 'root_child_dad_mom', 'root_child_dad_mom_dad', 'root_child_dad_mom_mom', 'root_child_dad_dad'])
        self.assertEqual(allg_parents, real_allgparents)
        self.assertEqual(len(allg_parents), 12)
        
    def test_all_grandparents_error(self):
        allg_parents = set([Person.get_persons_name(i) for i in self.root_child.all_grandparents()])
        ## I used the set before I fixed the all_granndparents code
        real_b_allgparents = set(['root_child_dad_dad_mom', 'root_child_dad_mom_dad', 'root_child_dad_mom_mom', 'root_child_mom_daa_dad', 'root_child_sister_dad_mom', 'root_child_mom_mum_dad', 'root_child_mom_mom_mom', 'root_child_dad_dad_dad'])
        self.assertNotEqual(allg_parents, real_b_allgparents)
        self.assertNotEqual(len(allg_parents), len(real_b_allgparents))
        
    def test_all_ancestors(self):
        ## First get list of all ancestors
        all_ancestors = set([Person.get_persons_name(i) for i in self.root_child.all_ancestors()])
        ##print(all_ancestors)
        real_all_ancestors = set(['root_child_mom', 'root_child_mom_dad_dad', 'root_child_mom_dad_mom', 'root_child_dad_dad', 'root_child_mom_mom_dad', 'root_child_dad_mom', 'root_child_mom_mom_mom', 'root_child_dad_dad_dad', 'root_child_dad_dad_mom', 'root_child_dad_mom_dad', 'root_child_dad_mom_mom', 'root_child_mom_dad', 'root_child_mom_mom', 'root_child_dad'])
        self.assertEqual(all_ancestors, real_all_ancestors)
        
    def test_all_ancestors_error(self):
        all_ancestors = set([Person.get_persons_name(i) for i in self.root_child.all_ancestors()])
        real_b_allancestors = set(['root_child_mom', 'root_child_mom_dad_dad', 'root_child_mom_dad_mom', 'root_child_dfud_dad', 'root_child_mom_mom_dad', 'root_child_dad_mom', 'root_child_mom_mom_mom', 'root_chiaodjflld_dad_dad_dad', 'root_child_dad_dad_mom', 'root_chightld_dad_mom_dad', 'root_child_dad_mom_mom', 'root_child_mom_dad', 'root_child_mom_mom', 'root_child_dad'])
        self.assertNotEqual(all_ancestors, real_b_allancestors)
        
    def test_ancestors(self):
        selfs_ancestors = [Person.get_persons_name(i) for i in self.root_child.ancestors(1,4)]
        self.assertEqual(len(selfs_ancestors), 14)
        
    def test_ancestors_error(self):
        with self.assertRaises(PersonError) as context:
            self.root_child.ancestors(2,1)
        self.assertIn('max_depth', str(context.exception))
        self.assertIn('cannot be less than min_depth', str(context.exception))
        

    ## Parents function had a bug and it is fixed
    def test_parents(self):
        root_child_parents = set([Person.get_persons_name(i) for i in self.root_child.parents()])
        self.assertEqual(len(root_child_parents), 2)
        
        
        
if __name__ == '__main__':
    unittest.main()