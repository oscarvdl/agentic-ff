namespace Shop.Orders;

public class Order
{
    public Guid Id { get; init; }
    public IReadOnlyList<OrderLine> Lines { get; init; } = [];

    public decimal CalculateVatAmount(string countryCode) =>
        Lines.Sum(l => l.UnitPrice * l.Quantity) * VatRateFor(countryCode);

    private static decimal VatRateFor(string countryCode) => countryCode switch
    {
        "NL" => 0.21m,
        "DE" => 0.19m,
        "FR" => 0.20m,
        "ES" => 0.21m,
        _ => 0.20m,
    };
}

public record OrderLine(string Sku, int Quantity, decimal UnitPrice);
