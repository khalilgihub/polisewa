const { poolPromise } = require('./db');

async function seed() {
    try {
        const pool = await poolPromise;
        console.log("Updating properties with natural humanlike student rental descriptions...");
        
        await pool.request().query("DELETE FROM properties");

        const query = `
            INSERT INTO properties (user_id, name, [desc], price, phone, lat, lng, image, is_verified, details)
            VALUES 
            (32, 'Bilik Sewa Taman Sri Matang', 'Kemasukan segera sem depan! Bilik non-sharing Taman Sri Matang, 3 minit jak pegi Politeknik Kuching. Bilik ada tilam single, kipas, meja study & almari. Rumah lengkap peti ais, mesin basuh & wifi. Student lelaki muslim diutamakan. Wasap utk fast deal.', '280', '0128892341', 1.5840, 110.3390, '["https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600", "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=600"]', 1, 'WiFi, Mesin Basuh, Peti Ais, Dapur Masak, Parking Moto'),
            (32, 'Bilik Pelajar Matang Hilir', 'Bilik bajet mesra student PKS. Sewa RM250 sebulan dah masuk api air. Ada katil + tilam. Jalan kaki 5 minit ke kedai makan, dobi layan diri & bus stop. Senang nak ulang-alik kelas. Sesuai utk student sem 1-5.', '250', '0198765432', 1.5895, 110.3540, '["https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600"]', 1, 'Api & Air Termasuk, Kipas, Berdekatan Dobi, Kedai Makan'),
            (34, 'Bilik Master Matang Jaya', 'Bilik master luas sharing 2 org / boleh request sorang. Ada bilik air sendiri dalam bilik, ada aircond & water heater. Rumah baru cat, bersih & selamat ada pagar. Selesa utk study. Boleh datang tengok bilik dulu.', '290', '0138217654', 1.5620, 110.3320, '["https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600"]', 1, 'Aircond, Bilik Air Sendiri, Water Heater, Pagar Automatik');
        `;

        await pool.request().query(query);
        console.log("Successfully updated properties with authentic descriptions!");
        
        const res = await pool.request().query("SELECT id, name, price, phone, [desc] FROM properties");
        console.log("Updated properties:", res.recordset);
        process.exit(0);
    } catch (err) {
        console.error("Error updating properties:", err);
        process.exit(1);
    }
}

seed();
