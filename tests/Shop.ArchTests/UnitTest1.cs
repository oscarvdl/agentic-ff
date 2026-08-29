using NetArchTest.Rules;
using Xunit;

namespace Shop.ArchTests;

public class BoundaryTests
{
    [Fact]
    public void Orders_Should_Not_Depend_On_Billing()
    {
        var result = Types.InAssembly(typeof(Orders.Class1).Assembly)
            .That().ResideInNamespace("Shop.Orders")
            .ShouldNot().HaveDependencyOn("Shop.Billing")
            .GetResult();

        Assert.True(result.IsSuccessful,
            $"Boundary violated by: {string.Join(", ", result.FailingTypeNames ?? new List<string>())}");
    }
}
