#include "pch.h"
#include "CppUnitTest.h"
#include <list>
#include "../Lab.11/Lab.11.cpp"
bool fill_list(std::list<int>& l, int count);
using namespace Microsoft::VisualStudio::CppUnitTestFramework;
namespace ListUnitTests
{
    TEST_CLASS(ListFillTests)
    {
    public:
        TEST_METHOD(TestListSizeAfterFilling)
        {
            std::list<int> my_list;
            int elements_to_add = 5;
            bool result = fill_list(my_list, elements_to_add);
            Assert::IsTrue(result);
            Assert::AreEqual(elements_to_add, static_cast<int>(my_list.size()));
        }

        TEST_METHOD(TestListElementsContent)
        {
            std::list<int> my_list;
            int elements_to_add = 3;
            fill_list(my_list, elements_to_add);
            auto it = my_list.begin();
            Assert::AreEqual(0, *it);
            int second_element = *(++it); 
            Assert::AreEqual(1, second_element);
            int third_element = *(++it);  
            Assert::AreEqual(2, third_element);
        }

        TEST_METHOD(TestFillingZeroElements)
        {
            std::list<int> my_list;
            bool result = fill_list(my_list, 0);
            Assert::IsTrue(result);
            Assert::IsTrue(my_list.empty());
            Assert::AreEqual(0, static_cast<int>(my_list.size()));
        }
    };
}
