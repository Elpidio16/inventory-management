import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    const totalProducts = await prisma.product.count();
    
    const inventoryData = await prisma.inventory.findMany({
      include: {
        product: true,
      },
    });

    const totalQuantity = inventoryData.reduce((sum, inv) => sum + inv.quantity, 0);
    
    const totalValue = await prisma.product.findMany({
      include: {
        inventory: true,
      },
    });

    const totalPrice = totalValue.reduce((sum, product) => {
      return sum + (product.price * (product.inventory?.quantity || 0));
    }, 0);

    const categoriesData = await prisma.category.findMany({
      include: {
        products: {
          include: {
            inventory: true,
          },
        },
      },
    });

    const categoriesWithStats = categoriesData.map(cat => ({
      id: cat.id,
      name: cat.name,
      description: cat.description,
      productCount: cat.products.length,
      totalQuantity: cat.products.reduce((sum, p) => sum + (p.inventory?.quantity || 0), 0),
      products: cat.products.map(p => ({
        id: p.id,
        name: p.name,
        price: p.price,
        quantity: p.inventory?.quantity || 0,
      })),
    }));

    return NextResponse.json({
      totalProducts,
      totalQuantity,
      totalPrice,
      categories: categoriesWithStats,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch inventory stats' },
      { status: 500 }
    );
  }
}
